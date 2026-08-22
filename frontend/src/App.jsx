import { useEffect, useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [token, setToken] = useState(
    localStorage.getItem("access_token")
  );

  const [applications, setApplications] = useState([]);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [adding, setAdding] = useState(false);

  const [newApplication, setNewApplication] = useState({
    company: "",
    position: "",
    status: "Applied",
    location: "",
    job_url: "",
    notes: "",
  });

  useEffect(() => {
    if (token) {
      loadApplications();
    }
  }, [token]);

  async function handleLogin(event) {
    event.preventDefault();

    setLoading(true);
    setMessage("");

    try {
      const response = await fetch(`${API_URL}/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: email,
          password: password,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        setMessage(data.detail || "Login failed");
        return;
      }

      localStorage.setItem("access_token", data.access_token);

      setToken(data.access_token);
      setEmail("");
      setPassword("");
    } catch (error) {
      setMessage("Could not connect to the HireTrack server.");
    } finally {
      setLoading(false);
    }
  }

  async function loadApplications() {
    try {
      const response = await fetch(`${API_URL}/applications`, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await response.json();

      if (!response.ok) {
        if (response.status === 401) {
          localStorage.removeItem("access_token");
          setToken(null);
          setApplications([]);
          setMessage("Your session expired. Please log in again.");
        }

        return;
      }

      setApplications(data);
    } catch (error) {
      setMessage("Could not load applications.");
    }
  }

  function handleApplicationChange(event) {
    const { name, value } = event.target;

    setNewApplication((currentApplication) => ({
      ...currentApplication,
      [name]: value,
    }));
  }

  async function handleAddApplication(event) {
    event.preventDefault();

    setAdding(true);
    setMessage("");

    try {
      const response = await fetch(`${API_URL}/applications`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(newApplication),
      });

      const data = await response.json();

      if (!response.ok) {
        setMessage(data.detail || "Could not add application");
        return;
      }

      setNewApplication({
        company: "",
        position: "",
        status: "Applied",
        location: "",
        job_url: "",
        notes: "",
      });

      await loadApplications();

      setMessage("Application added successfully.");
    } catch (error) {
      setMessage("Could not connect to the HireTrack server.");
    } finally {
      setAdding(false);
    }
  }

  function handleLogout() {
    localStorage.removeItem("access_token");

    setToken(null);
    setApplications([]);
    setMessage("");
  }

  if (token) {
    return (
      <div className="dashboard-page">
        <header className="dashboard-header">
          <div>
            <h1>HireTrack</h1>
            <p>Your job application dashboard</p>
          </div>

          <button
            className="logout-button"
            onClick={handleLogout}
          >
            Log out
          </button>
        </header>

        <main className="dashboard-content">
          <section className="add-section">
            <h2>Add Application</h2>

            <form
              className="application-form"
              onSubmit={handleAddApplication}
            >
              <div className="form-grid">
                <div>
                  <label htmlFor="company">Company</label>
                  <input
                    id="company"
                    name="company"
                    type="text"
                    value={newApplication.company}
                    onChange={handleApplicationChange}
                    required
                  />
                </div>

                <div>
                  <label htmlFor="position">Position</label>
                  <input
                    id="position"
                    name="position"
                    type="text"
                    value={newApplication.position}
                    onChange={handleApplicationChange}
                    required
                  />
                </div>

                <div>
                  <label htmlFor="status">Status</label>
                  <select
                    id="status"
                    name="status"
                    value={newApplication.status}
                    onChange={handleApplicationChange}
                  >
                    <option value="Applied">Applied</option>
                    <option value="Interview">Interview</option>
                    <option value="Offer">Offer</option>
                    <option value="Rejected">Rejected</option>
                  </select>
                </div>

                <div>
                  <label htmlFor="location">Location</label>
                  <input
                    id="location"
                    name="location"
                    type="text"
                    value={newApplication.location}
                    onChange={handleApplicationChange}
                  />
                </div>

                <div className="full-width">
                  <label htmlFor="job_url">Job URL</label>
                  <input
                    id="job_url"
                    name="job_url"
                    type="url"
                    value={newApplication.job_url}
                    onChange={handleApplicationChange}
                  />
                </div>

                <div className="full-width">
                  <label htmlFor="notes">Notes</label>
                  <textarea
                    id="notes"
                    name="notes"
                    rows="3"
                    value={newApplication.notes}
                    onChange={handleApplicationChange}
                  />
                </div>
              </div>

              <button
                className="primary-button"
                type="submit"
                disabled={adding}
              >
                {adding ? "Adding..." : "Add Application"}
              </button>
            </form>
          </section>

          {message && (
            <p className="dashboard-message">{message}</p>
          )}

          <section className="applications-section">
            <div className="dashboard-title">
              <div>
                <h2>Applications</h2>
                <p>
                  You have {applications.length} application
                  {applications.length !== 1 ? "s" : ""}.
                </p>
              </div>
            </div>

            {applications.length === 0 ? (
              <div className="empty-state">
                <h3>No applications yet</h3>
                <p>Add your first job application above.</p>
              </div>
            ) : (
              <div className="applications-list">
                {applications.map((application) => (
                  <div
                    className="application-card"
                    key={application.id}
                  >
                    <div>
                      <h3>{application.company}</h3>
                      <p>{application.position}</p>
                    </div>

                    <span className="status">
                      {application.status}
                    </span>

                    {application.location && (
                      <p className="location">
                        {application.location}
                      </p>
                    )}
                  </div>
                ))}
              </div>
            )}
          </section>
        </main>
      </div>
    );
  }

  return (
    <div className="page">
      <div className="login-card">
        <div className="brand">
          <h1>HireTrack</h1>
          <p>Track your job applications in one place.</p>
        </div>

        <form
          className="login-form"
          onSubmit={handleLogin}
        >
          <label htmlFor="email">Email</label>

          <input
            id="email"
            type="email"
            placeholder="you@example.com"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            required
          />

          <label htmlFor="password">Password</label>

          <input
            id="password"
            type="password"
            placeholder="Enter your password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            required
          />

          <button
            className="primary-button"
            type="submit"
            disabled={loading}
          >
            {loading ? "Logging in..." : "Log in"}
          </button>
        </form>

        {message && <p className="message">{message}</p>}
      </div>
    </div>
  );
}

export default App;