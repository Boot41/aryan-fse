// /home/aryan/Documents/project/client/src/routes/MyProfile.jsx

import React from 'react';
import ProfileInfo from '../components/profile/ProfileInfo';
import StudentScores from '../components/profile/StudentScores';
import TeacherClasses from '../components/profile/TeacherClasses';

const MyProfile = () => {
  // Sample data for development
  const profile = {
    name: 'John Doe',
    email: 'john.doe@example.com',
    role: 'student',
    profilePhoto: 'https://via.placeholder.com/150',
    averageScores: [
      { subject: 'Mathematics', score: 85.5 },
      { subject: 'Physics', score: 78.0 },
      { subject: 'Chemistry', score: 92.3 },
    ],
    classes: [
      { subject: 'Mathematics', students: 25 },
      { subject: 'Physics', students: 18 },
    ],
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 p-8">
      <h2 className="text-4xl font-bold text-center text-white mb-8">My Profile</h2>
      <div className="max-w-2xl mx-auto">
        {/* Profile Information */}
        <ProfileInfo profile={profile} />

        {/* Display Student Scores or Teacher Classes */}
        {profile.role === 'student' ? (
          <StudentScores averageScores={profile.averageScores} />
        ) : (
          <TeacherClasses classes={profile.classes} />
        )}
      </div>
    </div>
  );
};

export default MyProfile;