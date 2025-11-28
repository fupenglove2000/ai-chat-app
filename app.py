import streamlit as st
from config import config, Config
from chat_service import chat_service


# Page configuration
st.set_page_config(
    page_title="AI Chat Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
    }
    .assistant-message {
        background-color: #f5f5f5;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chat_mode" not in st.session_state:
        st.session_state.chat_mode = "assistant"
    if "total_tokens" not in st.session_state:
        st.session_state.total_tokens = 0


def clear_chat():
    """Clear chat history"""
    st.session_state.messages = []
    st.session_state.total_tokens = 0


def render_sidebar():
    """Render the sidebar with settings"""
    with st.sidebar:
        st.title("⚙️ Settings")

        # Chat mode selection
        st.subheader("Chat Mode")
        mode = st.selectbox(
            "Select assistant type:",
            options=list(Config.SYSTEM_PROMPTS.keys()),
            format_func=lambda x: x.capitalize(),
            key="mode_select"
        )

        if mode != st.session_state.chat_mode:
            st.session_state.chat_mode = mode
            st.rerun()

        # Display current mode description
        st.info(Config.SYSTEM_PROMPTS[st.session_state.chat_mode])

        st.divider()

        # Token counter
        st.subheader("📊 Statistics")
        st.metric("Messages", len(st.session_state.messages))
        st.metric("Estimated Tokens", st.session_state.total_tokens)

        st.divider()

        # Clear chat button
        if st.button("🗑️ Clear Chat", use_container_width=True):
            clear_chat()
            st.rerun()

        st.divider()

        # API key status
        st.subheader("🔑 API Status")
        if config.OPENAI_API_KEY:
            st.success("API Key configured")
        else:
            st.error("API Key not set")
            st.caption("Set OPENAI_API_KEY in .env file")


def render_chat():
    """Render the chat interface"""
    st.title("🤖 AI Chat Assistant")
    st.caption(f"Mode: {st.session_state.chat_mode.capitalize()}")

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        if not config.OPENAI_API_KEY:
            st.error("Please set your OpenAI API key in the .env file")
            return

        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            try:
                system_prompt = Config.SYSTEM_PROMPTS[st.session_state.chat_mode]

                # Stream the response
                for chunk in chat_service.chat_stream(
                    st.session_state.messages,
                    system_prompt=system_prompt
                ):
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")

                message_placeholder.markdown(full_response)

            except Exception as e:
                error_msg = f"Error: {str(e)}"
                message_placeholder.error(error_msg)
                full_response = error_msg

        # Add assistant response to history
        st.session_state.messages.append({"role": "assistant", "content": full_response})

        # Update token count
        st.session_state.total_tokens = chat_service.count_messages_tokens(st.session_state.messages)


def main():
    """Main application entry point"""
    initialize_session_state()
    render_sidebar()
    render_chat()


if __name__ == "__main__":
    main()
