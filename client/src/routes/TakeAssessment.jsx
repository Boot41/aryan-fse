// /home/aryan/Documents/project/client/src/routes/TakeAssessment.jsx

import React, { useState } from 'react';
import AssessmentQuestion from '../components/assessments/AssessmentQuestion';

const TakeAssessment = () => {
  // Sample assessment data for development
  const [assessment] = useState({
    title: 'Mathematics Quiz',
    questions: [
      {
        id: 1,
        question: 'What is 2 + 2?',
        options: ['3', '4', '5', '6'],
        correctAnswer: '4',
      },
      {
        id: 2,
        question: 'What is the square root of 16?',
        options: ['2', '3', '4', '5'],
        correctAnswer: '4',
      },
      {
        id: 3,
        question: 'What is 10 / 2?',
        options: ['2', '3', '4', '5'],
        correctAnswer: '5',
      },
    ],
  });

  const [answers, setAnswers] = useState({});

  const handleAnswerChange = (questionId, selectedOption) => {
    setAnswers((prevAnswers) => ({
      ...prevAnswers,
      [questionId]: selectedOption,
    }));
  };

  const handleSubmit = () => {
    // TODO: Submit answers to the backend
    console.log('Submitted Answers:', answers);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 p-8">
      <h2 className="text-4xl font-bold text-center text-white mb-8">{assessment.title}</h2>
      <div className="max-w-2xl mx-auto space-y-6">
        {assessment.questions.map((question) => (
          <AssessmentQuestion
            key={question.id}
            question={question}
            selectedAnswer={answers[question.id]}
            onAnswerChange={handleAnswerChange}
          />
        ))}
        <button
          onClick={handleSubmit}
          className="bg-gradient-to-r from-purple-700 to-indigo-700 text-white py-3 px-6 rounded-lg shadow-md hover:from-purple-800 hover:to-indigo-800 focus:outline-none focus:ring-2 focus:ring-purple-600 focus:ring-offset-2 transition-all duration-200 w-full"
        >
          Submit Assessment
        </button>
      </div>
    </div>
  );
};

export default TakeAssessment;