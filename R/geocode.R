# Adapted from: https://github.com/mlipper/geoclient-examples/tree/main/python/pandas
# Author of original: Edgar Alfonseca
# Modified for Geoclient v2 (NYC API) and R

library(httr)
library(jsonlite)
library(dplyr)

# Replace with your subscription key
GEOCLIENT_KEY <- Sys.getenv("GEOCLIENT_KEY")
GEOCLIENT_URL <- "https://api.nyc.gov/geoclient/v2"




bldg_to_geocode = bldg %>%
    select(b_id, b_zip, boro, b_block, b_lot, bbl_dhcr_bldg,
           # 3 address combinations
           b_street_no1, b_street_name1, b_street_sfx1,
           b_street_no2, b_street_name2, b_street_sfx2,
           b_street_no3, b_street_name3, b_street_sfx3
    ) %>%
    geoclient::geo_address_data(
        house_number = b_street_no1,
        street = b_street_name1,
        borough = boro,
        zip = b_zip)



# Sample data.frame
df <- data.frame(
    row_id = 1:2,
    bin_input = c("4538327", "3255603"),
    stringsAsFactors = FALSE
)

# Function to send API request and return parsed JSON response
send_request <- function(bin_input) {
    if (GEOCLIENT_KEY == "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx") {
        GEOCLIENT_KEY <- Sys.getenv("GEOCLIENT_KEY")
        if (GEOCLIENT_KEY == "") {
            stop("GEOCLIENT_KEY is still set to the default and an environment variable of the same name has not been set.")
        }
    }

    url <- paste0(GEOCLIENT_URL, "/bin")
    response <- GET(
        url,
        query = list(bin = bin_input),
        add_headers(
            `Cache-Control` = "no-cache",
            `Ocp-Apim-Subscription-Key` = GEOCLIENT_KEY
        )
    )

    if (status_code(response) == 200) {
        res_json <- content(response, as = "text", encoding = "UTF-8")
        res_list <- fromJSON(res_json, flatten = TRUE)
        return(res_list$bin)  # return only the 'bin' part of the response
    } else {
        return(list())  # empty list if request fails
    }
}

# Iterate over rows and get API responses
results <- lapply(df$bin_input, send_request)

# Convert list of results to data.frame
response_df <- bind_rows(results)
response_df$row_id <- df$row_id

# Join original df with the response
input_geocoded_df <- left_join(df, response_df, by = "row_id")

# View the resulting data.frame
print(input_geocoded_df)
