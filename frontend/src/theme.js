import { createTheme } from "@mui/material/styles";

export const appTheme = createTheme({
  palette: {
    mode: "light",
    primary: {
      main: "#8a5c36",
      dark: "#5a3a23",
      light: "#b98a61",
    },
    secondary: {
      main: "#1d3f5f",
    },
    background: {
      default: "#efe7dc",
      paper: "#f8f3eb",
    },
    text: {
      primary: "#2c2118",
      secondary: "#5c4b3f",
    },
  },
  typography: {
    fontFamily: '"Merriweather", "Georgia", serif',
    h4: {
      fontWeight: 700,
      letterSpacing: "0.02em",
    },
    h6: {
      fontWeight: 700,
    },
    button: {
      textTransform: "none",
      fontWeight: 700,
    },
  },
  shape: {
    borderRadius: 14,
  },
});
