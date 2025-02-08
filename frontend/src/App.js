import React, { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [projects, setProjects] = useState([]);

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/projects")
      .then(response => {
        console.log("API Response:", response.data);
        setProjects(response.data.projects);
      })
      .catch(error => console.error("Error fetching data:", error));
  }, []);

  return (
    <div>
      <h1>My Portfolio</h1>
      <ul>
        {projects.length > 0 ? (
          projects.map((project, index) => (
            <li key={index}>
              <h2>{project[1]}</h2> {/* title */}
              <p>{project[2]}</p> {/* description */}
              <a href={project[3]} target="_blank" rel="noopener noreferrer">GitHub</a>
            </li>
          ))
        ) : (
          <p>No projects found.</p>
        )}
      </ul>
    </div>
  );
}

export default App;
