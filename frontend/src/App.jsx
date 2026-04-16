import { useEffect, useMemo, useState } from "react";
import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  Container,
  Divider,
  Grid,
  List,
  ListItem,
  ListItemText,
  Paper,
  Stack,
  Typography,
} from "@mui/material";
import RestartAltIcon from "@mui/icons-material/RestartAlt";
import MemoryIcon from "@mui/icons-material/Memory";
import SportsEsportsIcon from "@mui/icons-material/SportsEsports";
import UndoIcon from "@mui/icons-material/Undo";
import { apiGet, apiPost } from "./api";

const FILES = ["a", "b", "c", "d", "e", "f", "g", "h"];
const RANKS = [8, 7, 6, 5, 4, 3, 2, 1];

function squareName(row, col) {
  return `${FILES[col]}${8 - row}`;
}

export default function App() {
  const [state, setState] = useState(null);
  const [selectedSquare, setSelectedSquare] = useState(null);
  const [legalTargets, setLegalTargets] = useState([]);
  const [banner, setBanner] = useState({
    severity: "info",
    text: "Loading board...",
  });
  const [loading, setLoading] = useState(false);

  const sideLabel = state ? (state.to_move === "w" ? "White" : "Black") : "-";

  const board = useMemo(() => state?.board ?? [], [state]);

  async function refreshState(message = null, severity = "info") {
    const data = await apiGet("/api/state");
    setState(data);
    if (message) {
      setBanner({ severity, text: message });
    }
  }

  useEffect(() => {
    refreshState().catch((err) => {
      setBanner({ severity: "error", text: err.message });
    });
  }, []);

  async function fetchLegal(square) {
    const data = await apiGet(`/api/legal/${square}`);
    setLegalTargets(data.targets || []);
  }

  async function performMove(fromSquare, toSquare) {
    setLoading(true);
    try {
      const res = await apiPost("/api/move", {
        from_square: fromSquare,
        to_square: toSquare,
      });
      setState(res.state);
      setBanner({
        severity: res.ok ? "success" : "warning",
        text: res.message,
      });
      setSelectedSquare(null);
      setLegalTargets([]);
    } catch (err) {
      setBanner({ severity: "error", text: err.message });
    } finally {
      setLoading(false);
    }
  }

  async function toggleAi(target) {
    setLoading(true);
    try {
      const res = await apiPost("/api/command", {
        command: `ai ${target ? "on" : "off"}`,
      });
      setState(res.state);
      setBanner({
        severity: res.ok ? "success" : "warning",
        text: res.message,
      });
    } catch (err) {
      setBanner({ severity: "error", text: err.message });
    } finally {
      setLoading(false);
    }
  }

  async function resetGame() {
    setLoading(true);
    try {
      const res = await apiPost("/api/reset");
      setState(res.state);
      setBanner({ severity: "info", text: res.message });
      setSelectedSquare(null);
      setLegalTargets([]);
    } catch (err) {
      setBanner({ severity: "error", text: err.message });
    } finally {
      setLoading(false);
    }
  }

  async function undoMove() {
    setLoading(true);
    try {
      const res = await apiPost("/api/undo");
      setState(res.state);
      setBanner({
        severity: res.ok ? "success" : "warning",
        text: res.message,
      });
      setSelectedSquare(null);
      setLegalTargets([]);
    } catch (err) {
      setBanner({ severity: "error", text: err.message });
    } finally {
      setLoading(false);
    }
  }

  async function onSquareClick(row, col) {
    if (!state || loading) {
      return;
    }

    const clicked = squareName(row, col);

    if (selectedSquare && legalTargets.includes(clicked)) {
      await performMove(selectedSquare, clicked);
      return;
    }

    if (selectedSquare === clicked) {
      setSelectedSquare(null);
      setLegalTargets([]);
      return;
    }

    const piece = board?.[row]?.[col];
    if (!piece) {
      setSelectedSquare(null);
      setLegalTargets([]);
      return;
    }

    const expected = state.to_move;
    if (piece.color !== expected) {
      setBanner({
        severity: "warning",
        text: "Select a piece of the side to move.",
      });
      return;
    }

    setSelectedSquare(clicked);
    fetchLegal(clicked).catch(() => {
      setLegalTargets([]);
    });
  }

  return (
    <Box
      className="app-shell"
      sx={{
        display: "flex",
        flexDirection: "column",
        height: "100vh",
        overflow: "hidden",
      }}
    >
      <Container
        maxWidth="100%"
        sx={{
          p: { xs: 1, sm: 1.5, md: 2 },
          width: "100%",
          height: "100%",
          display: "flex",
          flexDirection: "column",
          maxWidth: "100%",
        }}
      >
        <Paper className="top-banner" elevation={0}>
          <Stack
            direction={{ xs: "column", md: "row" }}
            spacing={2}
            alignItems={{ xs: "flex-start", md: "center" }}
            justifyContent="space-between"
          >
            <Box>
              <Typography variant="h4">Chess Studio</Typography>
              <Typography variant="subtitle1" color="text.secondary">
                Tactical boardroom for serious play
              </Typography>
            </Box>
            <Stack
              direction="row"
              spacing={1.5}
              alignItems="center"
              flexWrap="wrap"
            >
              <Chip label={state?.status || "Loading..."} color="secondary" />
              <Chip
                label={`Turn: ${sideLabel || "-"}`}
                color="primary"
                variant="outlined"
              />
              <Button
                startIcon={<RestartAltIcon />}
                variant="contained"
                onClick={resetGame}
                disabled={loading}
              >
                Reset
              </Button>
            </Stack>
          </Stack>
        </Paper>

        <Box
          sx={{
            flex: 1,
            minHeight: 0,
            mt: { xs: 0.5, sm: 1 },
            display: "flex",
            flexDirection: { xs: "column", md: "row" },
            gap: { xs: 1, md: 0 },
            alignItems: "stretch",
            justifyContent: "space-between",
            overflow: { xs: "auto", md: "visible" },
          }}
        >
          <Box
            sx={{
              width: { xs: "100%", md: "18%" },
              display: "flex",
              flexDirection: "column",
              flexShrink: 0,
              minHeight: { xs: "auto", md: "100%" },
              gap: 1,
            }}
          >
            <Card
              elevation={0}
              sx={{ flexGrow: 0, display: "flex", flexDirection: "column" }}
            >
              <CardContent
                sx={{
                  flexGrow: 1,
                  display: "flex",
                  flexDirection: "column",
                  p: 1.5,
                }}
              >
                <Stack direction="row" spacing={1} alignItems="center" mb={1.5}>
                  <MemoryIcon color="secondary" />
                  <Typography variant="h6">AI</Typography>
                </Stack>
                <Stack direction="column" spacing={1}>
                  <Button
                    fullWidth
                    variant={state?.ai_enabled ? "contained" : "outlined"}
                    startIcon={<SportsEsportsIcon />}
                    onClick={() => toggleAi(true)}
                    disabled={loading}
                    size="small"
                  >
                    On
                  </Button>
                  <Button
                    fullWidth
                    variant={!state?.ai_enabled ? "contained" : "outlined"}
                    onClick={() => toggleAi(false)}
                    disabled={loading}
                    size="small"
                  >
                    Off
                  </Button>
                </Stack>
              </CardContent>
            </Card>
            <Card
              elevation={0}
              sx={{ flexGrow: 1, display: "flex", flexDirection: "column" }}
            >
              <CardContent
                sx={{
                  flexGrow: 1,
                  display: "flex",
                  flexDirection: "column",
                  p: 1,
                }}
              >
                <Typography variant="body2" sx={{ mb: 1, fontWeight: "bold" }}>
                  Black Captured
                </Typography>
                <Box
                  sx={{
                    display: "flex",
                    flexWrap: "wrap",
                    gap: 0.5,
                    flex: 1,
                    overflow: "auto",
                    alignContent: "flex-start",
                  }}
                >
                  {(state?.captured_black || []).map((piece, idx) => (
                    <Box
                      key={idx}
                      sx={{
                        fontSize: "1.5rem",
                        lineHeight: 1,
                        p: 0.5,
                        backgroundColor: "rgba(200, 160, 120, 0.2)",
                        borderRadius: "4px",
                      }}
                    >
                      {piece.symbol}
                    </Box>
                  ))}
                </Box>
              </CardContent>
            </Card>
          </Box>

          <Box
            sx={{
              flex: 1,
              minHeight: 0,
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              mx: { xs: 0, md: 1 },
              minWidth: { xs: "100%", md: "400px" },
            }}
          >
            <Card
              className="board-card"
              elevation={0}
              sx={{
                width: "100%",
                height: "100%",
                maxHeight: "90vh",
                display: "flex",
                flexDirection: "column",
              }}
            >
              <CardContent
                sx={{
                  p: { xs: 0.75, sm: 1 },
                  "&:last-child": { pb: 1 },
                  flex: 1,
                  display: "flex",
                  justifyContent: "center",
                  alignItems: "center",
                  minHeight: 0,
                }}
              >
                <Box className="board-frame">
                  <Box className="board-grid">
                    {RANKS.map((rank, rowIndex) =>
                      FILES.map((file, colIndex) => {
                        const row = rowIndex;
                        const col = colIndex;
                        const square = `${file}${rank}`;
                        const piece = board?.[row]?.[col];
                        const dark = (row + col) % 2 === 1;
                        const isSelected = selectedSquare === square;
                        const isLegal = legalTargets.includes(square);

                        return (
                          <Box
                            key={square}
                            onClick={() => onSquareClick(row, col)}
                            className={`square ${dark ? "dark" : "light"} ${isSelected ? "selected" : ""} ${isLegal ? "legal" : ""}`}
                            aria-label={`square-${square}`}
                          >
                            {col === 0 && (
                              <span className="rank-label">{rank}</span>
                            )}
                            {row === 7 && (
                              <span className="file-label">{file}</span>
                            )}
                            <span
                              className={`piece ${piece?.color === "b" ? "black" : "white"}`}
                            >
                              {piece?.symbol || ""}
                            </span>
                            {isLegal && <span className="legal-dot" />}
                          </Box>
                        );
                      }),
                    )}
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Box>

          <Box
            sx={{
              width: { xs: "100%", md: "18%" },
              display: "flex",
              flexDirection: "column",
              flexShrink: 0,
              minHeight: { xs: "auto", md: "100%" },
              gap: 1,
            }}
          >
            <Card
              elevation={0}
              sx={{ flexGrow: 1, display: "flex", flexDirection: "column" }}
            >
              <CardContent
                sx={{
                  flexGrow: 1,
                  display: "flex",
                  flexDirection: "column",
                  p: 1,
                }}
              >
                <Typography variant="body2" sx={{ mb: 1, fontWeight: "bold" }}>
                  White Captured
                </Typography>
                <Box
                  sx={{
                    display: "flex",
                    flexWrap: "wrap",
                    gap: 0.5,
                    flex: 1,
                    overflow: "auto",
                    alignContent: "flex-start",
                  }}
                >
                  {(state?.captured_white || []).map((piece, idx) => (
                    <Box
                      key={idx}
                      sx={{
                        fontSize: "1.5rem",
                        lineHeight: 1,
                        p: 0.5,
                        backgroundColor: "rgba(200, 160, 120, 0.2)",
                        borderRadius: "4px",
                      }}
                    >
                      {piece.symbol}
                    </Box>
                  ))}
                </Box>
              </CardContent>
            </Card>
            <Card
              elevation={0}
              sx={{ flexGrow: 1, display: "flex", flexDirection: "column" }}
            >
              <CardContent
                sx={{
                  flexGrow: 1,
                  display: "flex",
                  flexDirection: "column",
                  overflow: "auto",
                  p: 1,
                }}
              >
                <Stack
                  direction="row"
                  spacing={1}
                  alignItems="center"
                  justifyContent="space-between"
                  mb={1}
                >
                  <Typography variant="h6">History</Typography>
                  <Button
                    size="small"
                    variant="outlined"
                    startIcon={<UndoIcon />}
                    onClick={undoMove}
                    disabled={loading || (state?.history || []).length === 0}
                  >
                    Undo
                  </Button>
                </Stack>
                <Divider sx={{ mb: 1 }} />
                <List
                  dense
                  className="history-list"
                  sx={{ flexGrow: 1, overflow: "auto" }}
                >
                  {(state?.history || []).length === 0 && (
                    <ListItem>
                      <ListItemText primary="No moves" />
                    </ListItem>
                  )}
                  {(state?.history || []).map((mv, idx) => {
                    const moveNumber = Math.floor(idx / 2) + 1;
                    const isWhite = idx % 2 === 0;
                    return (
                      <ListItem key={`${mv}-${idx}`} disablePadding>
                        <ListItemText
                          primary={
                            <Box component="span">
                              {isWhite && <strong>{moveNumber}.</strong>}{" "}
                              <span
                                style={{
                                  color: isWhite ? "#203f5c" : "#666",
                                  fontWeight: isWhite ? "bold" : "normal",
                                }}
                              >
                                {mv}
                              </span>
                            </Box>
                          }
                        />
                      </ListItem>
                    );
                  })}
                </List>
              </CardContent>
            </Card>
          </Box>
        </Box>

        <Box mt={{ xs: 1, sm: 1.5 }} flexShrink={0}>
          <Alert severity={banner.severity} sx={{ m: 0 }}>
            {banner.text}
          </Alert>
        </Box>
      </Container>
    </Box>
  );
}
