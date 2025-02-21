// /home/aryan/Documents/project/client/src/components/ProfileInfo.jsx

import React from 'react';

const ProfileInfo = ({ profile }) => {
  return (
    <div className="bg-gray-800/70 backdrop-blur-sm p-8 rounded-lg shadow-2xl border border-gray-700/30 mb-8">
      <div className="flex items-center space-x-8">
        {/* Profile Photo */}
        <img
          src={profile.profilePhoto}
          alt="Profile"
          className="w-32 h-32 rounded-full object-cover border-4 border-purple-700"
        />

        {/* Profile Details */}
        <div className="space-y-4">
          <div>
            <p className="text-sm font-medium text-gray-300">Name</p>
            <p className="text-white">{profile.name}</p>
          </div>
          <div>
            <p className="text-sm font-medium text-gray-300">Email</p>
            <p className="text-white">{profile.email}</p>
          </div>
          <div>
            <p className="text-sm font-medium text-gray-300">Role</p>
            <p className="text-white capitalize">{profile.role}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfileInfo;