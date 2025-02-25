// /home/aryan/Documents/project/client/src/components/AssessmentQuestion.jsx

import React from 'react';

const AssessmentQuestion = ({ question, selectedAnswer, onAnswerChange }) => {
  console.log(question)
  return (
    <div className="bg-gray-800/70 backdrop-blur-sm p-6 rounded-lg shadow-2xl border border-gray-700/30">
      <h3 className="text-xl font-semibold text-white mb-4">{question.question}</h3>
      <div className="space-y-3">
        {question.options.map((option, index) => (
          <label key={index} className="flex items-center space-x-3 cursor-pointer">
            <input
              type="radio"
              name={`question-${question.id}`}
              value={option}
              checked={selectedAnswer === option}
              onChange={() => onAnswerChange(question.id, option)}
              className="form-radio h-5 w-5 text-purple-600 focus:ring-purple-600"
            />
            <span className="text-gray-300">{option}</span>
          </label>
        ))}
      </div>
    </div>
  );
};

export default AssessmentQuestion;