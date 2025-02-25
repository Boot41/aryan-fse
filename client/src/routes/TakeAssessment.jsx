// /home/aryan/Documents/project/client/src/routes/TakeAssessment.jsx

import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import AssessmentQuestion from '../components/assessments/AssessmentQuestion';
import { getAssignmentQuestions, takeAssignment } from '../api';

const TakeAssessment = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const assignmentId = location.state?.assignmentId;

  const [assessment, setAssessment] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [answers, setAnswers] = useState({});

  useEffect(() => {
    const fetchAssignment = async () => {
      if (!assignmentId) {
        setError('No assignment selected');
        setLoading(false);
        return;
      }

      try {
        const data = await getAssignmentQuestions(assignmentId);
        console.log(JSON.parse(data.questions))
        setAssessment(JSON.parse(data.questions));
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };

    fetchAssignment();
  }, [assignmentId]);

  const handleAnswerChange = (questionId, selectedOption) => {
    setAnswers((prevAnswers) => ({
      ...prevAnswers,
      [questionId]: selectedOption,
    }));
  };

  const handleSubmit = async () => {
    if (!assignmentId) {
      setError('No assignment selected');
      return;
    }

    try {
      const studentEmail = localStorage.getItem('userEmail');
      // Calculate score based on correct answers
      const totalQuestions = assessment.questions.length;
      const correctAnswers = assessment.questions.filter(
        q => answers[q.id] === q.correctAnswer
      ).length;
      const score = (correctAnswers / totalQuestions) * 100;

      await takeAssignment({
        student_email: studentEmail,
        assignment_id: assignmentId,
        score: score
      });

      // Navigate back to assignments page after submission
      navigate('/assignments');
    } catch (error) {
      setError(error.message);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 p-8">
        <div className="text-4xl font-bold text-center text-white">Loading assessment...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 p-8">
        <div className="text-4xl font-bold text-center text-red-500">{error}</div>
      </div>
    );
  }

  if (!assessment) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 p-8">
        <div className="text-4xl font-bold text-center text-white">No assessment found</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 p-8">
      <h2 className="text-4xl font-bold text-center text-white mb-8">{assessment.title}</h2>
      <div className="max-w-2xl mx-auto space-y-6">
        {assessment?.map((question) => (
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