import React, { useState, useEffect } from 'react';
import AssignmentCard from '../components/AssignmentCard';
import { getUserAssignments } from '../api';

const Assignments = () => {
  const [assignments, setAssignments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchAssignments = async () => {
      try {
        const response = await getUserAssignments();
        console.log(response)
        setAssignments(response.assignments);
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };

    fetchAssignments();
  }, []);

  if (loading) {
    return <div className="text-center p-4 text-white">Loading assignments...</div>;
  }

  if (error) {
    return <div className="text-red-500 text-center p-4">{error}</div>;
  }

  // Separate completed and pending assignments
  const completedAssignments = assignments.filter(a => a.status === 'completed');
  const pendingAssignments = assignments.filter(a => a.status !== 'completed');

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 p-8">
      <h2 className="text-4xl font-bold text-center text-white mb-8">Assignments</h2>

      {/* Pending Assignments */}
      <div className="mb-12">
        <h3 className="text-2xl font-bold text-white mb-6">Pending Assignments</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {pendingAssignments.length > 0 ? (
            pendingAssignments.map((assignment) => (
              <AssignmentCard key={assignment.id} assignment={assignment} />
            ))
          ) : (
            <p className="text-gray-400">No pending assignments.</p>
          )}
        </div>
      </div>

      {/* Completed Assignments */}
      <div>
        <h3 className="text-2xl font-bold text-white mb-6">Completed Assignments</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {completedAssignments.length > 0 ? (
            completedAssignments.map((assignment) => (
              <AssignmentCard key={assignment.id} assignment={assignment} />
            ))
          ) : (
            <p className="text-gray-400">No completed assignments.</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default Assignments;