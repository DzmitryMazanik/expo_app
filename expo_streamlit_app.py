import streamlit as st
from openai import OpenAI


api_key  = st.text_input("Введите API-ключ", type="password")

client = OpenAI(
    api_key=api_key,
)

model = "gpt-4o-mini"


# Initialize session state for partners if it doesn't exist
if 'partners' not in st.session_state:
    st.session_state.partners = None

# Ask the user to input the organization name
nas_org_name = st.text_input("Введите название вашей организации")

# Ask the user to input the description of the organization
nas_org_description = st.text_area("Направления деятельности вашей организации:")

# Ask the user for the number of partners to extract
n = st.number_input("Введите количество партнеров для рекомендации:", min_value=1, step=1)

# Ask the user to input the description of potential partners
partners_description = st.text_area("Введите текст с описанием предполагаемых партнеров")

example = """
BRILLAND MINING AND METALLURGY TECHNOLOGY LIMITED:
    - направления деятельности: горно-обогатительное оборудование, дробильно-сортировочные комплексы
    - направления для сотрудничества: обе организации занимаются разработкой дробильно-сортировочные комплексов - есть смысл проработать варианты сотрудничества по этому направлению
"""

find_partners_prompt = f"""
    Описание организации НАН Беларуси {nas_org_name}:{nas_org_description}
    Извлеки {n} самых релевантных потенциальных партнеров для {nas_org_name} с указанием схожих направлений деятельности и областей для сотрудничества из следующего текста: {partners_description}
    Пример:
    {example}   
    """

if st.button('Получить рекомендацию'):
    if nas_org_name and nas_org_description and partners_description and api_key:        
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": find_partners_prompt}
                    ]
                )
            
            st.session_state.partners = response.choices[0].message.content
            
            st.write("Потенциальные партнеры:")
            st.write(st.session_state.partners)

        except Exception as e:
            st.error(f"Ошибка: {str(e)}")
    else:
        st.write("Мы не можем дать рекомендацию без данных :(")

if st.button('Сформировать задания'):
    if nas_org_name and st.session_state.partners:
        task_example = """
        - представительство интересов НАН Беларуси для партнеров;
        - поиск потенциальных партнеров в сфере научной и производственной деятельности предприятия;
        - проведение переговоров представителями компаний по вопросам заключения контрактов;
        - подписание Соглашений о научно-техническом сотрудничестве.
        """
        
        task_prompt = f"""
        Составь список заданий на командировку для участия в международной выставке в части установления сотрудничества между {nas_org_name} и следующими организациями: {st.session_state.partners}
        Примеры заданий:
        {task_example}
        """
        
        try:
            task_response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": task_prompt}
                ]
            )
            
            tasks = task_response.choices[0].message.content
            
            # Display the generated tasks
            st.write("Задания на командировку:")
            st.write(tasks)
        
        except Exception as e:
            st.error(f"Ошибка: {str(e)}")
    else:
        st.write("Пожалуйста, сначала сформируйте список партнеров.")