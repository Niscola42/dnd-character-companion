import { createTheme } from '@mui/material/styles'

const displayFont = (
    '"Oswald", "Arial Narrow", sans-serif'
  )

export const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#9f2738',
      light: '#c24a5b',
      dark: '#671522',
      contrastText: '#fff7ed',
    },
    secondary: {
      main: '#b89656',
      light: '#d6bd83',
      dark: '#745b2d',
      contrastText: '#17120d',
    },
    error: {
      main: '#c44747',
    },
    warning: {
      main: '#c7833f',
    },
    success: {
      main: '#5f8f68',
    },
    background: {
      default: '#0d0b0c',
      paper: '#181416',
    },
    text: {
      primary: '#eee5d8',
      secondary: '#b8aa9b',
    },
    divider: 'rgba(184, 150, 86, 0.28)',
  },

  shape: {
    borderRadius: 6,
  },

  typography: {
    fontFamily: '"Roboto", sans-serif',

    h1: {
      fontFamily: displayFont,
      fontWeight: 700,
      letterSpacing: '0.02em',
    },
    h2: {
      fontFamily: displayFont,
      fontWeight: 700,
      letterSpacing: '0.02em',
    },
    h3: {
      fontFamily: displayFont,
      fontWeight: 700,
      letterSpacing: '0.02em',
    },
    h4: {
      fontFamily: displayFont,
      fontWeight: 700,
    },
    h5: {
      fontFamily: displayFont,
      fontWeight: 700,
      letterSpacing: '0.04em',
    },
    h6: {
      fontFamily: displayFont,
      fontWeight: 700,
      letterSpacing: '0.04em',
    },
    button: {
      fontWeight: 700,
      letterSpacing: '0.04em',
    },
  },

  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          backgroundImage: `
            radial-gradient(
              circle at top,
              rgba(103, 21, 34, 0.16),
              transparent 42%
            ),
            linear-gradient(
              180deg,
              #100d0f 0%,
              #0a090a 100%
            )
          `,
          backgroundAttachment: 'fixed',
        },
      },
    },

    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundImage: (
            'linear-gradient(90deg, #241318, #151113)'
          ),
          borderBottom: (
            '1px solid rgba(184, 150, 86, 0.35)'
          ),
          boxShadow: '0 8px 30px rgba(0, 0, 0, 0.4)',
        },
      },
    },

    MuiCard: {
      styleOverrides: {
        root: {
          backgroundImage: (
            'linear-gradient(145deg, #1d181a, #141113)'
          ),
          border: (
            '1px solid rgba(184, 150, 86, 0.22)'
          ),
          boxShadow: '0 12px 28px rgba(0, 0, 0, 0.28)',
        },
      },
    },

    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: (
            'linear-gradient(145deg, #1d181a, #141113)'
          ),
          border: (
            '1px solid rgba(184, 150, 86, 0.18)'
          ),
        },
      },
    },

    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
        },
      },
    },
  },
})