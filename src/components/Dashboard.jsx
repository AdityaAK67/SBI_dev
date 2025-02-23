import React from "react";
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, Tooltip, ResponsiveContainer, XAxis, YAxis, CartesianGrid, Legend } from "recharts";
import { Plus, Search,FileText , User, Power, X, Bell, RefreshCw } from "lucide-react";
import { useNavigate } from "react-router-dom";


const Dashboard = () => {
  const navigate = useNavigate();

  
    const handleOpenFile = () => {
      window.open("/demo.py", "_blank"); // Opens the file in a new tab
    };

  const dataAlerts = [
    { name: "Critical", value: 12, color: "#ff4d4d" },
    { name: "High", value: 5, color: "#ffcc00" },
    { name: "Low", value: 20, color: "#4caf50" },
  ];

  const data = [
    { month: "Jan", accuracy: 72 },
    { month: "Feb", accuracy: 74 },
    { month: "Mar", accuracy: 78 },
    { month: "Apr", accuracy: 81 },
    { month: "May", accuracy: 85 },
    { month: "Jun", accuracy: 87 },
    { month: "Jul", accuracy: 90 },
    { month: "Aug", accuracy: 92 },
    { month: "Sep", accuracy: 93 },
    { month: "Oct", accuracy: 94 },
    { month: "Nov", accuracy: 95 },
    { month: "Dec", accuracy: 96 },
  ];

  const trendData = [
    { name: "Jan", value: 20 },
    { name: "Feb", value: 18 },
    { name: "Mar", value: 15 },
    { name: "Apr", value: 12 },
    { name: "May", value: 10 },
  ];
  return (
    <div className="p-6 bg-[#0b0f35] min-h-screen text-white">

      {/* Navbar */}
      <nav className="flex justify-between items-center p-4 bg-slate-950 shadow-lg rounded-lg mb-6">
        <h1 className="text-2xl font-bold tracking-tighter leading-10">Security Monitoring Dashboard🛡️</h1>
        <div className="flex gap-6 items-center">
          <button className="relative hover:text-blue-500 transition duration-200 ease-in-out">
            <Bell className="text-white" size={22} />
            <span className="absolute top-0 right-0 bg-red-500 text-white text-xs rounded-full px-1">1</span>
          </button>
          
          <button
            className="flex items-center hover:text-blue-500 transition duration-200 ease-in-out text-white"
            onClick={() => navigate("/login")}
          >
            <User className="mr-2 text-white" size={20} />
            Login
          </button>

          <button
            className="flex items-center hover:text-blue-500 transition duration-200 ease-in-out text-white"
            onClick={() => navigate("/login")}
          >
            <FileText  className="mr-2 text-white" size={20} />
            Reports          
            </button>
          <button className="flex items-center hover:text-red-500 transition duration-200 ease-in-out">
            <Power className="mr-2 text-red-500" size={20} />
            Logout
          </button>
        </div>
      </nav>

      {/* Main Container */}
      <div className="bg-slate-950 rounded-xl shadow-md mb-6 flex flex-wrap lg:flex-nowrap justify-between items-center p-6">

        {/* Left: Line Graph */}
        <div className="w-full lg:w-1/3 mr-4 mt-10 mb-10 px-2">
          <h3 className="text-lg font-semibold text-white mb-4 text-center">AI-Predicted False Positives</h3>
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={trendData}>
              <XAxis dataKey="name" stroke="#ddd" />
              <YAxis stroke="#ddd" />
              <Tooltip />
              <Line type="monotone" dataKey="value" stroke="#22D3EE" strokeWidth={3} dot={{ r: 5, stroke: '#fff', strokeWidth: 2 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Middle: Textual Information */}
        <div className="w-full lg:w-1/3 text-center text-white space-y-6">
          <h2 className="text-2xl font-bold tracking-tight text-cyan-400">Unified Cybersecurity Dashboard 🔑</h2>
          <div className="bg-slate-900 p-4 rounded-lg hover:bg-slate-800 transition-all">Critical Vulnerabilities: <span className="text-red-500">🔴 12</span> <span className="text-orange-500">🟠 5</span> <span className="text-green-500">🟢 20</span></div>
          <div className="bg-slate-900 p-4 rounded-lg hover:bg-slate-800 transition-all">False Positives (AI-Predicted): 📉 Trend Line</div>
          <div className="bg-slate-900 p-4 rounded-lg hover:bg-slate-800 transition-all">CI/CD Blocked Deployments: 📊</div>
        </div>

        {/* Right: Bar Graph */}
        <div className="w-full lg:w-1/3 px-6">
          <h3 className="text-lg font-semibold text-white mt-8 mb-4 text-center">OWASP Top 10 Coverage: <span className="text-green-400">████████ 90%</span></h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={dataAlerts}>
              <CartesianGrid strokeDasharray="3 3" stroke="#444" />
              <XAxis dataKey="name" stroke="#ddd" />
              <YAxis stroke="#ddd" />
              <Tooltip />
              <Legend />
              <Bar dataKey="low" fill="#16A34A" stackId="a" />
              <Bar dataKey="medium" fill="#EAB308" stackId="a" />
              <Bar dataKey="high" fill="#DC2626" stackId="a" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>


      <div className="flex flex-wrap lg:flex-nowrap gap-6 mb-2">
        {/* Cloud & Pipeline Monitoring */}
        <div className="bg-slate-950 p-6 rounded-xl shadow-lg w-full lg:w-1/2 border border-slate-700 transition-all duration-300 hover:shadow-xl hover:border-blue-500">
          <h2 className="text-xl font-semibold mb-4 text-white flex items-center gap-2">
            ☁️ Cloud & Pipeline Monitoring
          </h2>

          {/* Cloud Scans */}
          <div className="bg-slate-900 p-3 rounded-md shadow-md transition-transform duration-200 hover:scale-105 cursor-pointer">
            <p className="text-slate-300 text-lg flex justify-between">
              <span>Cloud Scans Last 24h:</span>
              <span className="font-bold">
                ✅ <span className="text-green-400">15</span> ❌ <span className="text-red-400">2</span>
              </span>
            </p>
          </div>

          {/* CI/CD Pipeline Status */}
          <div className="bg-slate-900 p-3 rounded-md mt-3 shadow-md transition-transform duration-200 hover:scale-105 cursor-pointer">
            <p className="text-slate-300 text-lg">CI/CD Pipeline Status:</p>
            <ul className="ml-4 list-disc text-slate-300">
              <li className="transition-all hover:text-green-400">✅ Passed: <span className="font-bold">20</span></li>
              <li className="transition-all hover:text-red-400">🚫 Blocked: <span className="font-bold">3</span> (SonarQube Quality Gates)</li>
            </ul>
          </div>

          {/* Charts Section */}
          <div className="mt-4">
            <p className="text-slate-300 text-lg flex items-center gap-2 hover:text-blue-400 transition-all cursor-pointer">
              📈 Lambda Execution Time vs. Vulnerabilities Found
            </p>
            <p className="text-slate-300 text-lg flex items-center gap-2 hover:text-blue-400 transition-all cursor-pointer">
              📊 ZAP Scan Severity Distribution
            </p>
          </div>
        </div>

        {/* Code Health Overview */}
        <div className="bg-slate-950 p-6 rounded-xl shadow-lg w-full lg:w-1/2 border border-slate-700 transition-all duration-300 hover:shadow-xl hover:border-blue-500">
          <h3 className="text-xl font-extrabold mb-4 text-white tracking-tighter flex items-center gap-2">
            🛠️ Code Health Overview
          </h3>

          {/* Vulnerability Breakdown */}
          <p className="text-lg font-semibold mb-3 text-slate-300">⚠️ Vulnerability Breakdown</p>
          <div className="rounded-lg border border-slate-700 mx-auto mb-2 text-center w-72 h-12 flex items-center justify-center bg-slate-800 text-white shadow-md transition-transform duration-200  cursor-pointer">
            🐞 SQL Injection: <span className="text-red-400 font-bold ml-2">12</span>
          </div>
          <div className="rounded-lg border border-slate-700 mx-auto mb-2 text-center w-72 h-12 flex items-center justify-center bg-slate-700 text-white shadow-md transition-transform duration-200 cursor-pointer">
            🚨 XSS: <span className="text-yellow-400 font-bold ml-2">8</span>
          </div>
          <div className="rounded-lg border border-slate-700 mx-auto mb-4 text-center w-72 h-12 flex items-center justify-center bg-slate-800 text-white shadow-md transition-transform duration-200  cursor-pointer">
            🔗 Insecure Dependencies: <span className="text-orange-400 font-bold ml-2">5</span>
          </div>

          {/* Top Risky Files */}
          <p className="text-lg font-semibold mb-3 text-slate-300">📂 Top Risky Files</p>
          <div className="rounded-lg border border-slate-700 mx-auto mb-2 text-center w-72 h-12 flex items-center justify-center bg-slate-800 text-white shadow-md transition-transform duration-200 hover:scale-105 cursor-pointer">
            🔴 auth.py <span className="text-red-400 font-bold ml-2">(Critical)</span>
          </div>
          <div className="rounded-lg border border-slate-700 mx-auto mb-4 text-center w-72 h-12 flex items-center justify-center bg-slate-700 text-white shadow-md transition-transform duration-200 hover:scale-105 cursor-pointer">
            🟠 payment.js <span className="text-yellow-400 font-bold ml-2">(High)</span>
          </div>

          {/* Action Button */}
          <button onClick={handleOpenFile}  className="mt-4 px-5 py-2 bg-blue-600 rounded-lg text-white font-semibold shadow-lg hover:bg-blue-700 transition-all duration-300 flex items-center justify-center gap-2 hover:scale-105">
            🔍 View Code Snippet
          </button>
        </div>
      </div>



      {/* AI/ML Predictions */}
      <div className="bg-slate-950 mb-2 p-6 rounded-xl shadow-lg w-full border border-slate-700 transition-all duration-300 hover:shadow-xl hover:border-blue-500">
        <h2 className="text-xl font-semibold mb-4 text-white flex items-center gap-2">
          🤖 AI/ML Predictions
        </h2>

        {/* False Positive Reduction */}
        <div className="bg-slate-900 p-4 rounded-md shadow-md transition-transform duration-200 cursor-pointer">
          <p className="text-slate-300 text-lg">📉 False Positive Reduction:</p>
          <ul className="ml-4 list-disc text-slate-300 mt-2">
            <li className="hover:text-red-400">Before AI: <span className="font-bold">40%</span></li>
            <li className="hover:text-green-400">After AI: <span className="font-bold">12%</span></li>
          </ul>
        </div>

        {/* Top Predicted Threats */}
        <div className="bg-slate-900 p-4 rounded-md mt-3 shadow-md transition-transform duration-200 cursor-pointer">
          <p className="text-slate-300 text-lg">⚠️ Top Predicted Threats:</p>
          <ul className="ml-4 list-disc text-slate-300 mt-2">
            <li className="relative group cursor-pointer hover:text-yellow-400">
              Business Logic Flaws: <span className="font-bold">8</span>

              {/* Tooltip Content */}
              <div className="absolute left-0 mt-1 hidden bg-slate-950 group-hover:block text-white text-sm p-3 rounded-lg shadow-lg w-64">
                <ul className="list-disc ml-4 space-y-1">
                  <li>Bypassing payment validation</li>
                  <li>Unauthorized access to user data</li>
                  <li>Skipping order approval process</li>
                  <li>Altering product prices via API</li>
                </ul>
              </div>
            </li>
            <li className="hover:text-red-400">OWASP Top 10: <span className="font-bold">15</span></li>
          </ul>
        </div>

        {/* Model Accuracy Over Time */}
        <p className="mt-4 text-slate-300 text-lg flex items-center gap-2 hover:text-blue-400 transition-all cursor-pointer">
          📊 Model Accuracy Over Time: <span className="text-blue-300">📈 Trend Graph</span>
        </p>

        {/* Graph Section */}
        <div className="mt-4 bg-slate-900 p-4 rounded-lg shadow-md">
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={data}>
              <CartesianGrid strokeDasharray="3 3" stroke="gray" />
              <XAxis dataKey="month" stroke="white" />
              <YAxis stroke="white" domain={[70, 100]} />
              <Tooltip />
              <Line type="monotone" dataKey="accuracy" stroke="#38bdf8" strokeWidth={3} dot={{ r: 4, fill: "#38bdf8" }} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>


      <div className="bg-slate-950 p-6 rounded-xl shadow-lg w-full border border-slate-700 transition-all duration-300 hover:shadow-xl hover:border-blue-500">
        <h2 className="text-xl font-semibold mb-4 text-white flex items-center gap-2">
          📜 Compliance & Reporting
        </h2>

        {/* Compliance Status */}
        <div className="bg-slate-800 p-4 rounded-md shadow-md transition-transform duration-200  cursor-pointer">
          <p className="text-slate-300 text-lg">✅ Compliance Status:</p>
          <ul className="ml-4 list-disc text-slate-300 mt-2">
            <li className="hover:text-green-400">OWASP: <span className="font-bold">95%</span></li>
            <li className="hover:text-yellow-400">SANS: <span className="font-bold">88%</span></li>
            <li className="hover:text-blue-400">GDPR: <span className="font-bold">Compliant</span></li>
          </ul>
        </div>

        {/* Report Generation Button */}
        <button
          className="mt-4 px-5 py-2 bg-slate-900 rounded-lg text-white font-semibold shadow-lg hover:bg-blue-700 transition flex items-center justify-center gap-2"
          onClick={() => {
            const link = document.createElement("a");
            link.href = "/zap_scan_result_yuvatech.json"; // Path to file inside public/
            link.download = "zap_scan_result_yuvatech.json"; // File name when downloaded
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
          }}
        >
          📄 Generate Report (JSON)
        </button>

      </div>
    </div>
  );
};

export default Dashboard;