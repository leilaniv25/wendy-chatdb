# pip install langchain
# pip install langchain-community
# pip install ollama
from langchain_ollama.llms import OllamaLLM
from langchain_community.utilities import SQLDatabase
from langchain.prompts import FewShotPromptTemplate, PromptTemplate
# import pymysql
import re


# function to print the intro to the chatbot
def print_intro():
    print('─' * 60)
    print("Welcome to Wendy, Your Wearable Tech Expert")
    print('─' * 60)
    print("Wendy is very knowledgeable about a database that hold data")
    print("about data records from smartphones/smartwatches and ")
    print("data from a survey user completed that asked for the same")
    print("information the wearable device collected.\n")
    print("You can exit the app by responding with \"exit\"\n")

# function to take in the question and invoke llm
# return a cleaned SQL query
def prompt_llm(llm, schema, input_question):
    examples = [
        {
            "question": "List all users",
            "sql": "SELECT * FROM user_info;"
        },
        {
            "question": "What are the types of stress levels?",
            "sql": "SELECT DISTINCT stress_level FROM measured_stress_data;"
        },
        {
            "question": "Give 3 rows of data that a  wearable device measured",
            "sql": "SELECT * FROM measured_physical_data LIMIT 3;"
        },
    ]

    prompt_from_examples = PromptTemplate(
        input_variables=["question", "sql"],
        template="Q: {question}\nA: {sql}")

    prompt_query = FewShotPromptTemplate(
        examples=examples,
        example_prompt=prompt_from_examples,
        prefix="You are a SQL expert that writes SQL queries. Do not use subqueries. Do not use nested SELECT statements. Do not use COALESCE. Do not use CASE WHEN. Here's the schema:\n" + schema + "\n\n Examples: ",
        suffix="Q: {input}\nA:",
        input_variables=["input"]
    )

    formatted_prompt = prompt_query.format(input=input_question)
    result = llm.invoke(formatted_prompt)
    sql_query = re.findall(r"```sql\n(.*?)```", result, re.DOTALL)
    cleaned_sql_query = ""
    if sql_query.__len__() > 0:
        raw_sql_query = sql_query[-1]
        cleaned_sql_query = raw_sql_query.replace("\n", " ")
        if "SELECT" in cleaned_sql_query or "INSERT" in cleaned_sql_query or "UPDATE" in cleaned_sql_query or "DELETE" in cleaned_sql_query:
            print("\nSQL Query:", cleaned_sql_query)
        else:
            cleaned_sql_query = ""
    return cleaned_sql_query


def main():
    # set up the llm and the database
    llm = OllamaLLM(model="llama3.2:3b")
    mysql_uri = 'mysql+pymysql://root:doctorMin-515@localhost:3306/wearable_devices_dataset'
    db = SQLDatabase.from_uri(mysql_uri)

    # the database schema to give to the llm
    schema_text = """
    Tables:
    - user_info(user_id, wearable, age)
    - measured_physical_data(timestamp, user_id, height, weight, steps, calories, light_sleep, deep_sleep, rem_sleep)
    - measured_stress_data(timestamp, user_id, stress_level)
    - user_input_data(user_id, height, weight, steps, calories, light_sleep, deep_sleep, rem_sleep)

    Relationships:
    - user_info.user_id = measured_physical_data.user_id
    - user_info.user_id = measured_stress_data.user_id
    - user_info.user_id = user_input_data.user_id
    """

    schema = db.get_table_info()

    # introduction text
    print_intro()
    # variable for key word input
    input_text1 = ""

    # while loop that handles app logic
    while input_text1 != "exit":
        print('─' * 60)
        input_text1 = input("Would you like to explore, query, or modify the database? ")
        if input_text1 != "explore" and input_text1 != "query" and input_text1 != "modify" and input_text1 != "exit":
            print("Please enter explore, query, or modify.")
            continue
        if input_text1 == "exit":
            break
        elif input_text1 == "explore":
            input_question = input("What do you want to know about the database? ")
            # prompt to give to llm so that it returns a SQL query
            prompt_explore = f"""
                Here is a database schema:

                {schema_text}

                Answer this question about the schema:

                {input_question}
                """
            result = llm.invoke(prompt_explore)
            print(result)
            continue
        elif input_text1 == "query" or input_text1 == "modify":
            input_question = input("What do you want to query or modify about the database? ")
            cleaned_sql_query = prompt_llm(llm, schema, input_question)
            if cleaned_sql_query.__len__() <= 0: # could not find a SQL query, ask the llm again
                cleaned_sql_query = prompt_llm(llm, schema, input_question)
            # run SQL query
            if len(cleaned_sql_query) > 0:
                try:
                    db_response = db._execute(cleaned_sql_query)
                    if input_text1 == "modify":
                        if "SELECT" in cleaned_sql_query:
                            cleaned_sql_query = prompt_llm(llm, schema, input_question)
                            db_response = db._execute(cleaned_sql_query)
                        print("The database has been successfully modified.")
                    if input_text1 == "query":
                        if db_response.__len__() <= 0:
                            # try to execute one more time
                            cleaned_sql_query = prompt_llm(llm, schema, input_question)
                            db_response = db._execute(cleaned_sql_query)
                        # print('─' * 60)
                        print("Here are the results:\n")
                        for row in db_response:
                            print(row)
                        print("")
                except Exception as e:
                    print("Invalid SQL")
        else:
            print("Please enter explore, query, or modify.")
    # print ending phrase
    print("Thank you for using Wendy. Have a nice day!")

    '''
    Explore
    1. what are the tables in the database?
    2. what attributes are in the measured stress data table?
    - give me 3 sample rows from the measure physical data table
    Query
    3. how many total users are in the user info table?
    4. give me the first 3 users from the measured physical data table and order them by height descending with an offset of 2
    5. return the age and total count only of users from the measured stress data whose total number of “low” stress levels is greater than 30
    Modify
    6. add a user with id “270f67aKhg” that is 22 years old and wears a Mi Band 4
        7. how many total users are in the user info table?
    8. update the age of user “270f67aKhg” to 23 years old in the user info table
        9. give me the age of user "270f67aKhg" from the user info table / from the user info table, what is the age of user "270f67aKhg"?
    10. from the user info table, only delete the user “270f67aKhg”
        11. how many total users are in the user info table?
    '''


if __name__ == "__main__":
    main()