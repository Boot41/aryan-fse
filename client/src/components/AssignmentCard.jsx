// /home/aryan/Documents/project/client/src/components/assessments/AssessmentCard.jsx

import React from 'react';
import { useNavigate } from 'react-router-dom';

const AssignmentCard = ({ assignment }) => {
  const navigate = useNavigate();

  // console.log(assignment)
  const handleStartAssessment = () => {
    navigate('/take-assessment', { state: { assignmentId: assignment.id } }); // Pass assignment ID to the TakeAssessment page
  };

  return (
    <div className="bg-gray-800/70 backdrop-blur-sm p-6 rounded-lg shadow-2xl border border-gray-700/30">
      <h3 className="text-xl font-semibold text-white mb-4">{assignment?.title || 'Untitled Assessment'}</h3>
      <p className="text-gray-300 mb-4">{assignment?.description || 'No description available'}</p>

      {/* Display Test Data */}
      {assignment?.test_data && (
        <div className="text-gray-400 mb-4">
          <p>Duration: {assignment.test_data.duration}</p>
          <p>Total Questions: {assignment.test_data.totalQuestions}</p>
        </div>
      )}

      {/* Display Result and Completion Date if Attempted */}
      {assignment?.status === 'Completed' && (
        <>
          <p className="text-green-400 mb-2">Score: {assignment.result}</p>
          <p className="text-gray-400 mb-4">Completed on: {assignment.completionDate || 'Unknown Date'}</p>
        </>
      )}

      <div className="flex justify-between items-center">
        <span className="text-gray-400">{assignment?.status || 'Status Unknown'}</span>
        {assignment?.status === 'pending' && (
          <button
            onClick={handleStartAssessment}
            className="bg-gradient-to-r from-purple-700 to-indigo-700 text-white py-2 px-4 rounded-lg shadow-md hover:from-purple-800 hover:to-indigo-800 focus:outline-none focus:ring-2 focus:ring-purple-600 focus:ring-offset-2 transition-all duration-200"
          >
            Start Assessment
          </button>
        )}
      </div>
    </div>
  );
};

export default AssignmentCard;