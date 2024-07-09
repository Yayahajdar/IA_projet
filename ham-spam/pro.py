import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import ComplementNB
from sklearn.metrics import accuracy_score

def load_css(file_name = "style.css"):
    with open(file_name) as f:
        css = f'<style>{f.read()}</style>'
    return css
css = load_css()
st.markdown(css, unsafe_allow_html=True)


# Reading csv file
df = pd.read_csv('https://raw.githubusercontent.com/remijul/dataset/master/SMSSpamCollection', sep='\t', header=None)
df.rename(columns={0: 'sit', 1: 'correct'}, inplace=True)

# exploring the dataset
sit_value_counts = df['sit'].value_counts()


labels = ['ham', 'spam']
counts = [4825, 747]

# Calculate the percentage values
percentages = [count / sum(counts) * 100 for count in counts]

# Create a list of labels with both count and percentage
label_values = [f'{label}\n({count})' for label, count in zip(labels, counts)]

plt.pie(counts, labels=label_values, autopct='%1.1f%%', colors=['green', 'lightgreen'], startangle=90)

# Draw a circle in the center of the pie to make it look like a donut chart (optional)
centre_circle = plt.Circle((0,0),0.70,fc=(0.9 ,0.91, 0.75))
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
fig.set_facecolor('xkcd:salmon')
fig.set_facecolor((0.9 ,0.91, 0.75))
plt.title("Distribution of Spam and Ham" , size =25, color=('green'))

st.pyplot(fig)


# Separate classes
df_ham = df[df.sit == 'ham']
df_spam = df[df.sit == 'spam']

# Convert to list
ham_list = df_ham['correct'].tolist()
spam_list = df_spam['correct'].tolist()

# Convert the list into a string
fil_spam = ("").join(spam_list)
fil_spam = fil_spam.lower()

# Convert the list into a string
fil_ham = "".join(map(str, ham_list))
fil_ham = fil_ham.lower()

# Your dataset as a string or a list of strings
text_data = fil_spam

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df['correct'], df['sit'], test_size=0.2, random_state=42)

# Vectorize the data
vectorizer = CountVectorizer()
X_train_vectorized = vectorizer.fit_transform(X_train)
X_test_vectorized = vectorizer.transform(X_test)

# Train a classifier
model = ComplementNB(force_alpha=True)
model.fit(X_train_vectorized, y_train)

row_input = st.columns((4,1,1,1))
# username input at column 1
with row_input[0]:
    # username input
  new_email = st.text_area("Input your email or SMS:")


if 'clicked' not in st.session_state:
    st.session_state.clicked = False
def click_button():
    st.session_state.clicked = True
with row_input[2]:
 st.button('Validate', on_click=click_button , type="secondary")

if st.session_state.clicked:

  new_email_vectorized = vectorizer.transform([new_email])
  prediction = model.predict(new_email_vectorized)

  # Display the prediction
  st.write(f'The predicted label for the new email is: {prediction[0]}')
 
# Evaluate the model
predictions = model.predict(X_test_vectorized)
accuracy = accuracy_score(y_test, predictions)

# Display the accuracy
st.write(f'Model Accuracy: {accuracy}')


