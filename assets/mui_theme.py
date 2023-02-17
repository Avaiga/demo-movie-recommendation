##############################################################
#         CUSTOM MUI THEME
#         MUI doc : https://mui.com/material-ui/customization/default-theme
##############################################################

#### Defining colors

# Primary and secondary colors
color_primary = "#ff462b"
color_secondary = "#283282"

# Contextual color
color_error = "#FF595E"
color_warning= "#FAA916"
color_success = "#96E6B3"

# Background and elevation color for light mode
color_background_light = "#f1f1f1"
color_paper_light = "#ffffff"

# Background and elevation color for dark mode
color_background_dark = "#051924"
color_paper_dark = "#072636"

# Set main font family
font_family = "Lato, Arial, sans-serif"

# Matching input and button height
input_button_height = 48

# Base border radius
border_radius = 8

#################### Light theme specific  ####################

light_theme = {
  "palette": {
    "background": {
        # Main background
        "default": color_background_light,
        # Cards background
        "paper": color_paper_light
    }
  },
  "components": {
    # Give MuiSlider disabled thumb a fill color matching the theme
    "MuiSlider": {
      "styleOverrides": {
        "thumb": {
          ".Mui-disabled &::before": {
            "backgroundColor": color_paper_light,  
          }
        }
      }
    },
  }
}

#################### Dark theme specific ####################
dark_theme = {
  "palette": {
    "background": {
        # Main background
        "default": color_background_dark,
        # Cards background
        "paper": color_paper_dark
    }
  },
  "components": {
    # Give MuiSlider disabled thumb a fill color matching the theme
    "MuiSlider": {
      "styleOverrides": {
        "thumb": {
          ".Mui-disabled &::before": {
            "backgroundColor": color_paper_dark,  
          }
        }
      }
    },
  }
}

#################### Common theme ####################

common_theme = {
  "palette": {
    # Primary and secondary colors
    "primary": {
        "main": color_primary
    },
    "secondary": {
        "main": color_secondary
    },
    "error": {
        "main": color_error
    },
    "warning": {
        "main": color_warning
    },
    "success": {
        "main": color_success
    }
  },
  "typography": {
    # Custom font
    "fontFamily": font_family,
    "h6": {
      "fontSize": "1rem"
    }
  },
  "shape": {
    "borderRadius": border_radius
  },
  # Components normalization
  "components": {
    # Form control
    "MuiFormControl": {
      "styleOverrides": {
        "root": {
          # Fill the available width
          "display": "flex",

          "&.taipy-selector": {
            "marginLeft": 0,
            "marginRight": 0
          },

          # Removing vertical margins if placed in a layout to avoid y-alignment issues
          ".taipy-layout > .taipy-part > .md-para > &":{
            "&:first-child": {
              "marginTop": 0,
            },
            "&:last-child": {
              "marginBottom": 0
            }
          }
        },
      }
    },
    # Form label
    "MuiInputLabel": {
      "styleOverrides": {
        "outlined": {
          # Properly position floating label on Y axis (second translate value) as the input height changes
          "&:not(.MuiInputLabel-shrink)": {
            "transform": "translate(14px, 12px) scale(1)",
          }
        },
      }
    },
    # Form input
    "MuiInputBase": {
      "styleOverrides": {
        "root": {
          # Fill the available width
          "display": "flex",
        },
        "input": {
          "height": input_button_height,
          "boxSizing": "border-box",

          ".MuiInputBase-root &": {
            "paddingTop": 4,
            "paddingBottom": 4
          }
        }
      }
    },
    "MuiSelect": {
      "styleOverrides": {
        "select": {
          "display": 'flex',
          "alignItems": 'center',
          "height": input_button_height,
          "line-height": input_button_height,
          "boxSizing": "border-box",

          "&.MuiInputBase-input": {
            "paddingTop": 0,
            "paddingBottom": 0,
          }
        }
      }
    },
    # Button
    "MuiButtonBase": {
      "styleOverrides": {
        "root": {
          "height": input_button_height       
        }
      }
    },
    # Floating action button
    "MuiFab": {
      "styleOverrides": {
        "root": {
          ".taipy-file-download &": {
            "height": input_button_height,
            "paddingLeft": "1em",
            "paddingRight": "1em",
            "backgroundColor": "transparent",
            "borderWidth": 1,
            "borderColor": color_primary,
            "borderStyle": "solid",
            "borderRadius": border_radius,
            "boxShadow": "none",
            "color": color_primary,
          }
        }
      }
    },
    # Toggle button group
    "MuiToggleButtonGroup": {
      "styleOverrides": {
        "root": {
          "verticalAlign": "middle",  
        }
      }
    },
    # Mui list
    "MuiList": {
      "styleOverrides": {
        "root": {
          ".taipy-selector .MuiPaper-root &": {
            "backgroundColor": "transparent",
          } 
        }
      },
    },
    # Mui slider
    "MuiSlider": {
      "styleOverrides": {
        "rail": {
          ".taipy-indicator &": {
            # Use success and error color for heat gradient
            "background": "linear-gradient(90deg, " + color_error + " 0%, " + color_success + " 100%)"
          }
        }
      }
    },
  }
}
