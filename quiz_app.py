import streamlit as st
import pathlib
import random

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

NUM_QUESTIONS_PER_QUIZ = 10

st.title(":red[Chinh phục Sử Địa 6]")
st.markdown(
    """
    <style>
    .title-text {
        color: red; /* Màu chữ của tiêu đề */
    }
    </style>
    """,
    unsafe_allow_html=True
)

def main():
    if 'stage' not in st.session_state:
        st.session_state.stage = 0

    if 'questions_path' not in st.session_state:
        st.session_state.questions_path = None

    if 'selected_topic' not in st.session_state:
        st.session_state.selected_topic = None

    if 'questions' not in st.session_state:
        st.session_state.questions = []

    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0

    if 'answers' not in st.session_state:
        st.session_state.answers = []

    if 'submitted' not in st.session_state:
        st.session_state.submitted = False

    if 'ordered_alternatives' not in st.session_state:
        st.session_state.ordered_alternatives = []

    def set_state(i):
        st.session_state.stage = i

    def set_questions_path(path):
        st.session_state.questions_path = path

    def set_selected_topic(topic):
        st.session_state.selected_topic = topic

    def submit_quiz():
        st.session_state.submitted = True
        st.experimental_rerun()

    if st.session_state.stage == 0:
        s1, s2 = st.columns((0.7,1))
        s1.image("images\\ba-925x1299.png")
        s2.header(":red[**Chào mừng đến với \"Chinh phục Sử Địa 6\"**]", divider='rainbow')
        s2.markdown("*\"Chinh phục Sử Địa 6\"* – nơi bạn có thể thử sức với hàng loạt các bài trắc nghiệm"
                    " phong phú theo từng chương từ nội dung của sách \"Lịch sử và Địa lí 6 - Kết nối tri thức"
                    " với cuộc sống\". Hãy cũng nhau khám phá kiến thức và củng cố tri thức của bạn "
                    "qua các bài trắc nghiệm thú vị và bổ ích nhé!")
        s2.button(':rainbow[Bắt đầu thôi!!!]', on_click=set_state, args=[1])

    if st.session_state.stage == 1 or st.session_state.stage == 2:
        st.header(":red[Lựa chọn môn học]")
        st.subheader("Hãy lựa chọn môn học mà bạn muốn kiểm tra kiến thức", divider='rainbow')
        s1, s2 = st.columns((1, 1))
        s1.image("images\\l-1256x874.png", use_column_width="always")
        s2.image("images\\ls-1256x707.jpg", use_column_width="always")
        s1, s2 = st.columns((1, 1))
        s1.markdown("Kiểm tra và củng cố kiến thức về lịch sử qua 5 chương học khác nhau, từ lịch sử loài người "
                    "cho đến lịch sử Việt Nam.")
        s2.markdown("Thử thách kiến thức về địa lí của mình qua các câu hỏi đa dạng và hấp dẫn quay quanh địa lí"
                    " của Trái Đất.")
        if s1.button(":rainbow[Lịch sử ^.^]"):
            set_questions_path(pathlib.Path(__file__).parent / "BoCauHoiLichSu.toml")
            set_state(2)
        if s2.button(":rainbow[Địa lí 0.0]"):
            set_questions_path(pathlib.Path(__file__).parent / "BoCauHoiDiaLi.toml")
            set_state(2)

    if st.session_state.stage == 2:
        if st.session_state.questions_path:
            topics = get_topics(st.session_state.questions_path)
            st.header(":red[Chọn chương mà bạn muốn kiểm tra:]", divider='rainbow')
            selected_topic = st.selectbox("",topics)
            if st.button(':rainbow[Xác nhận chương]'):
                set_selected_topic(selected_topic)
                set_state(3)
                st.experimental_rerun()

    if st.session_state.stage == 3:

        if st.session_state.questions_path and st.session_state.selected_topic:
            questions = prepare_questions(st.session_state.questions_path, st.session_state.selected_topic, NUM_QUESTIONS_PER_QUIZ)
            st.session_state.questions = questions
            st.session_state.answers = [None] * NUM_QUESTIONS_PER_QUIZ
            st.session_state.ordered_alternatives = [
                random.sample([q["answer"]] + q["alternatives"], k=len([q["answer"]] + q["alternatives"]))
                for q in questions
            ]
            set_state(4)

    if st.session_state.stage == 4:
        if st.session_state.questions and not st.session_state.submitted:
            st.header("Hãy cố gắng hoàn thành bài kiểm tra thật nhanh nhé:", divider='rainbow')
            all_answers_selected = all(answer is not None for answer in st.session_state.answers)
            for i, question in enumerate(st.session_state.questions):
                ordered_alternatives = st.session_state.ordered_alternatives[i]
                st.subheader(f"Câu hỏi số {i + 1}")
                answer = st.radio(question["question"], ordered_alternatives, index=None, key=f"q{i}_answer")
                st.session_state.answers[i] = answer

            if st.button('Nộp bài'):
                if all_answers_selected:
                    submit_quiz()
                else:
                    st.warning("Vui lòng chọn tất cả các đáp án trước khi tiếp tục.")

        if st.session_state.submitted:
            num_correct = 0
            st.header("Kết quả:")
            for num, question in enumerate(st.session_state.questions, start=1):
                q = question["question"]
                st.subheader(f"Câu hỏi số {num}: {q}")
                st.write(f"Câu trả lời của bạn: {st.session_state.answers[num-1]}")
                correct_answer = question["answer"]
                answer = st.session_state.answers[num - 1]
                if answer == correct_answer:
                    num_correct += 1
                    st.write("⭐ :rainbow[Đáp án đúng!] ⭐")
                else:
                    st.write(f"Đáp án đúng là {correct_answer!r}, không phải {answer!r}")
            st.header(f"\nBạn đã trả lời đúng {num_correct}/{NUM_QUESTIONS_PER_QUIZ} câu hỏi!")
            if st.button('Làm lại'):
                set_state(0)
                st.session_state.submitted = False
                st.session_state.current_question = 0
                st.experimental_rerun()
def get_topics(questions_path):
    topic_info = tomllib.loads(questions_path.read_text('utf-8'))
    topics = [topic["label"] for topic in topic_info.values()]
    return topics

def prepare_questions(path, selected_topic, num_questions):
    topic_info = tomllib.loads(path.read_text('utf-8'))
    questions = [question for topic in topic_info.values() if topic["label"] == selected_topic for question in topic["questions"]]
    num_questions = min(num_questions, len(questions))
    return random.sample(questions, k=num_questions)

if __name__ == "__main__":
    main()
