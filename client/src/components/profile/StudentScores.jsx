// /home/aryan/Documents/project/client/src/components/StudentScores.jsx

import React from 'react';

const StudentScores = ({ averageScores }) => {
  return (
    <div className="bg-gray-800/70 backdrop-blur-sm p-8 rounded-lg shadow-2xl border border-gray-700/30">
      <div className="space-y-4">
        {averageScores.length > 0 ? (
          averageScores.map((subject, index) => (
            <div key={index} className="flex justify-between items-center">
              <p className="text-white">{subject.subject}</p>
              <p className="text-white">{subject.score}%</p>
            </div>
          ))
        ) : (
          <p className="text-gray-400">No scores available.</p>
        )}
      </div>
    </div>
  );
};

export default StudentScores;