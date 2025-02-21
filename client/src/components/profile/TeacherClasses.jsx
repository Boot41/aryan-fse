// /home/aryan/Documents/project/client/src/components/TeacherClasses.jsx

import React from 'react';

const TeacherClasses = ({ classes }) => {
  return (
    <div className="bg-gray-800/70 backdrop-blur-sm p-8 rounded-lg shadow-2xl border border-gray-700/30">
      <div className="space-y-4">
        {classes.length > 0 ? (
          classes.map((cls, index) => (
            <div key={index} className="flex justify-between items-center">
              <p className="text-white">{cls.subject}</p>
              <p className="text-white">{cls.students} students</p>
            </div>
          ))
        ) : (
          <p className="text-gray-400">No classes assigned.</p>
        )}
      </div>
    </div>
  );
};

export default TeacherClasses;