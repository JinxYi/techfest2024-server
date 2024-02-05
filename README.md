# SallyRise

![SallyRise Logo](static\logo.jpg)

## Setup

1.Set up the database using the following command at the project root directory:

```bash
python setup.py
```

2.To run the web server, go to the project root directory and type the following:

```bash
python -m flask --app server run
```

## Introducing SallyRise

SallyRise: Your Ultimate Academic Companion
Overview:SallyRise is a comprehensive educational platform developed by our dynamic team—Divya, Jingyi, Chuanyou, and Yewint. It’s designed to be the ultimate academic companion in a world saturated with technological advancements.
Team Number: 67
Reference Code: 7G
Features:

1. Summariser: Simplifies extensive paragraphs into concise key points, facilitating easy digestion of information. Uses Artifical Intelligence in the form of NLP which decodes and tokenizes the words into numbers and finds number-matching patterns forming a string of numbers that result in a sentence. This process results in a concise summary.
2. QnA Flashcard: Generates personalized questions and answers based on the user’s topic, providing an instant recap after reading the summarized content. The QnA Flashcard uses Artificial Intelligence in a similar manner to the Summariser. All generated flashcards are securely stored in a MySQL database for future reference. We used a pre-trained open source model from HuggingFace community for the above 2 features.
3. Sally: A chatbot that adds a personalized touch to the learning experience. Through real-time conversations, students can seek clarification, ask questions about their studies, or engage in meaningful discussions on various topics. We used a pre-existing large language model and changed the features accordingly to suit our dataset.
4. Intuitive user interface and interactive design: We used Flask as a framework to render our front and back-ends of our web application. We have implemented a dark mode, as it is preferred by most students.
Scalability:SallyRise scales effortlessly across mobile and web platforms, ensuring accuracy with increased user input. Future plans include accommodating larger documents, offline access, and AI-generated flowcharts as part of image generation.
Vision:
Our vision extends beyond conventional boundaries, with plans to offer premium features for monetization. SallyRise caters to a diverse demographic, including students, parents, teachers, and employees, fostering a remote application that knows no geographical limits.
ConclusionIn conclusion, SallyRise is not just an innovation; it represents a revolutionary step in education technology. We invite you to join us on this journey of transforming learning experiences and making education accessible to all.
Let’s rise with Sally!
