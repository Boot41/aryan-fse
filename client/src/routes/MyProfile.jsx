import React, { useState, useEffect } from 'react';
import { getUserProfile } from '../services/api';
import ProfileInfo from '../components/profile/ProfileInfo';
import StudentScores from '../components/profile/StudentScores';
import TeacherClasses from '../components/profile/TeacherClasses';

const MyProfile = () => {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const data = await getUserProfile();
        setProfile(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 p-8 flex items-center justify-center">
        <div className="text-white text-xl">Loading profile...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 p-8 flex items-center justify-center">
        <div className="text-red-500 text-xl">Error: {error}</div>
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 p-8 flex items-center justify-center">
        <div className="text-white text-xl">No profile data available</div>
      </div>
    );
  }

  // Transform the stats data for the components
  const studentStats = {
    ...profile,
    averageScores: [
      { 
        subject: 'Overall',
        score: profile.stats.average_score
      }
    ]
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 p-8">
      <h2 className="text-4xl font-bold text-center text-white mb-8">My Profile</h2>
      <div className="max-w-4xl mx-auto">
        {/* Profile Information */}
        <ProfileInfo profile={profile} />

        {/* Display Student Scores or Teacher Classes */}
        {profile.role === 'student' ? (
          <div className="space-y-8">
            <StudentScores averageScores={studentStats.averageScores} />
            <div className="bg-gray-800/70 backdrop-blur-sm rounded-lg p-6 text-white border border-gray-700/30">
              <h3 className="text-xl font-semibold mb-4">Assignment Statistics</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <p className="text-gray-400">Total Assignments</p>
                  <p className="text-2xl">{profile.stats.total_assignments}</p>
                </div>
                <div>
                  <p className="text-gray-400">Completed</p>
                  <p className="text-2xl">{profile.stats.completed_assignments}</p>
                </div>
                <div>
                  <p className="text-gray-400">Pending</p>
                  <p className="text-2xl">{profile.stats.pending_assignments}</p>
                </div>
              </div>
            </div>
          </div>
        ) : (
          <TeacherClasses classes={[]} />
        )}
      </div>
    </div>
  );
};

export default MyProfile;