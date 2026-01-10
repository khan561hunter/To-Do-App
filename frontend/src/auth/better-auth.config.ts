export const betterAuthConfig = {
  // Better Auth configuration stub for JWT strategy
  // In a real implementation with Better Auth, this would involve
  // configuring providers and database adapters.
  // For this MVP, we are using the backend JWT for simplicity as allowed.
};

export const getAuthToken = () => {
  if (typeof window !== "undefined") {
    return localStorage.getItem("todo_token");
  }
  return null;
};

export const logout = () => {
  if (typeof window !== "undefined") {
    localStorage.removeItem("todo_token");
    window.location.href = "/login";
  }
};
