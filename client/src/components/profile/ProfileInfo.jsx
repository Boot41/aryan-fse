// /home/aryan/Documents/project/client/src/components/ProfileInfo.jsx

import React from 'react';

const ProfileInfo = ({ profile }) => {
  // Default avatar if no profile photo is provided
  const defaultAvatar = "https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp&f=y";

  return (
    <div className="bg-gray-800/70 backdrop-blur-sm p-8 rounded-lg shadow-2xl border border-gray-700/30 mb-8">
      <div className="flex flex-col md:flex-row items-center md:space-x-8">
        {/* Profile Photo */}
        <img
          src={profile.profile_photo || defaultAvatar}
          alt="Profile"
          className="w-32 h-32 rounded-full object-cover border-4 border-purple-700 mb-4 md:mb-0"
        />

        {/* Profile Details */}
        <div className="space-y-4 text-center md:text-left">
          <div>
            <p className="text-sm font-medium text-gray-300">Name</p>
            <p className="text-white text-lg">{profile.name || profile.username}</p>
          </div>
          <div>
            <p className="text-sm font-medium text-gray-300">Email</p>
            <p className="text-white">{profile.email}</p>
          </div>
          <div>
            <p className="text-sm font-medium text-gray-300">Role</p>
            <p className="text-white capitalize">{profile.role}</p>
          </div>
          <div>
            <p className="text-sm font-medium text-gray-300">Member Since</p>
            <p className="text-white">{new Date(profile.created_at).toLocaleDateString()}</p>
          </div>
        </div>

        {/* Additional Stats */}
        <div className="mt-6 md:mt-0 md:ml-auto text-center md:text-right">
          <div className="bg-purple-700/20 rounded-lg p-4">
            <p className="text-sm font-medium text-gray-300">Overall Progress</p>
            <p className="text-3xl font-bold text-white">
              {profile.stats ? 
                Math.round((profile.stats.completed_assignments / (profile.stats.total_assignments || 1)) * 100) 
                : 0}%
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfileInfo;