/*
 * DEVELOPER: Branis
 * RESPONSIBILITY: Existing authentication API service.
 *
 * TASKS:
 * - Maintain the login and registration requests.
 * - Maintain the logout request.
 * - Maintain the current-user/session verification request.
 * - Ensure authentication errors are handled consistently.
 *
 * INTEGRATION:
 * - Coordinate with Vincent on shared API configuration.
 * - Preserve the currently working authentication flow.
 * - Do not create a second authentication implementation.
 * - Do not modify App.jsx.
 */

const API_URL = "http://localhost:5000/api/auth";

async function request(endpoint, options = {}) {
  let response;

  try {
    response = await fetch(`${API_URL}${endpoint}`, {
      ...options,
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
    });
  } catch {
    throw new Error(
      "Cannot connect to the server. Make sure the Flask backend is running."
    );
  }

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(data.error || "Something went wrong. Please try again.");
  }

  return data;
}

export function registerUser(userData) {
  return request("/signup", {
    method: "POST",
    body: JSON.stringify(userData),
  });
}

export function loginUser(credentials) {
  return request("/login", {
    method: "POST",
    body: JSON.stringify(credentials),
  });
}

export function getCurrentUser() {
  return request("/me", {
    method: "GET",
  });
}

export function logoutUser() {
  return request("/logout", {
    method: "POST",
  });
}
