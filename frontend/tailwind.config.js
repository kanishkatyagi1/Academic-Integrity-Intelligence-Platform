// TailwindCSS content and theme configuration for the AIIP frontend.
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#1b1f2a",
        panel: "#f7f9fc",
        ibm: "#0f62fe",
      },
      boxShadow: {
        soft: "0 18px 50px rgba(22, 34, 51, 0.12)",
      },
    },
  },
  plugins: [],
};
