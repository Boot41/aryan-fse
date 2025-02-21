// /home/aryan/Documents/project/client/src/api.js

// Temporary data for development
const temporaryData = {
  assessments: [
    {
      id: 1,
      title: "Mathematics Quiz",
      description: "A quiz covering basic algebra and geometry.",
      status: "Upcoming",
      result: null,
      test_data: {
        duration: "30 minutes",
        totalQuestions: 10,
      },
    },
    {
      id: 2,
      title: "Physics Test",
      description: "Test on Newtonian mechanics and thermodynamics.",
      status: "Completed",
      result: "85%",
      completionDate: "2025-02-20",
      test_data: {
        duration: "1 hour",
        totalQuestions: 20,
      },
    },
  ],
  profile: {
    name: "John Doe",
    email: "john.doe@example.com",
    role: "student",
    profilePhoto: "https://via.placeholder.com/150",
    averageScores: [
      { subject: "Mathematics", score: 85.5 },
      { subject: "Physics", score: 78.0 },
      { subject: "Chemistry", score: 92.3 },
    ],
    classes: [
      { subject: "Mathematics", students: 25 },
      { subject: "Physics", students: 18 },
    ],
  },
  chatbot: {
    startConversation: () => {
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve({ success: true, message: "Conversation started" });
        }, 1000);
      });
    },
    endConversation: () => {
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve({ success: true, message: "Conversation ended" });
        }, 1000);
      });
    },
  },
};

// API stubs
export const fetchAssessments = () => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(temporaryData.assessments);
    }, 1000);
  });
};

export const fetchProfile = () => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(temporaryData.profile);
    }, 1000);
  });
};

export const startChatbotConversation = () => {
  return temporaryData.chatbot.startConversation();
};

export const endChatbotConversation = () => {
  return temporaryData.chatbot.endConversation();
};
