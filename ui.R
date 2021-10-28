# Import R packages needed for the UI
library(shiny)
library(shinycssloaders)
library(DT)

# Begin UI for the R + reticulate example app
ui <- fluidPage(
  
  titlePanel('Example app: Using R Shiny + reticulate'),
  
  sidebarLayout(
    
    # ---------------- Sidebar panel with changeable inputs ----------------- #
    sidebarPanel(
      width = 2,
      textInput('symbol', 'Symbol', value = 'SPY,^IXIC'),
      dateRangeInput('dateRange', separator = "",
                     label = 'Date range: yyyy-mm-dd',
                     start = '2020-01-01', end = Sys.Date()),
      selectInput("graph", "Graph type",
                  c("value","cumulative % change"),
                  selected = "cumulative % change"),
      selectInput("price", "Price type",
                  c("Open", "High", "Low", "Close", "Adj Close", "Volume"),
                  selected = "Close"),
    ),
    
    # ---------------- Sidebar panel with changeable inputs ----------------- #
    mainPanel(
      width = 10,
      # Output: Tabset w/ plot, summary, and table ----
      tabsetPanel(type = 'tabs',
                  tabPanel('Chart',
                           withSpinner(imageOutput('stockchart'))),
                  tabPanel('Prices',
                           withSpinner(verbatimTextOutput('stockdata'))),
                  tabPanel('Plotly',
                           includeHTML("Crypto_Report.html")),
                  tabPanel('System', 
                           h3('Current system info'),
                           '(These values will change when app is run locally vs on Shinyapps.io)',
                           hr(),
                           withSpinner(DT::dataTableOutput('sysinfo')),
                           br(),
                           verbatimTextOutput('pythoninfo')
                  )
      )
    )
  )
)