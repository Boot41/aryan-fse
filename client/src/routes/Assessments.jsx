// /home/aryan/Documents/project/client/src/routes/Assessments.jsx

import React from 'react';
import AssessmentCard from '../components/assessments/AssessmentCard';

import { useEffect, useState } from 'react';
import { fetchAssessments } from '../api';

const Assessments = () => {
  const [assessments, setAssessments] = useState([]);

  useEffect(() => {
    fetchAssessments().then((data) => setAssessments(data));
  }, []);
  // Separate attempted and un-attempted assessments
  const unAttemptedAssessments = assessments.filter((a) => a.result === null);
  const attemptedAssessments = assessments.filter((a) => a.result !== null);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 p-8">
      <h2 className="text-4xl font-bold text-center text-white mb-8">Assessments</h2>

      {/* Un-attempted Assessments */}
      <div className="mb-12">
        <h3 className="text-2xl font-bold text-white mb-6">Upcoming Assessments</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {unAttemptedAssessments.length > 0 ? (
            unAttemptedAssessments.map((assessment) => (
              <AssessmentCard key={assessment.id} assessment={assessment} isAttempted={false} />
            ))
          ) : (
            <p className="text-gray-400">No upcoming assessments.</p>
          )}
        </div>
      </div>

      {/* Attempted Assessments */}
      <div>
        <h3 className="text-2xl font-bold text-white mb-6">Completed Assessments</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {attemptedAssessments.length > 0 ? (
            attemptedAssessments.map((assessment) => (
              <AssessmentCard key={assessment.id} assessment={assessment} isAttempted={true} />
            ))
          ) : (
            <p className="text-gray-400">No completed assessments.</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default Assessments;