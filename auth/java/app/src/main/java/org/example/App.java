package org.example;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.http.HttpHeaders;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;

public class App {

    static final String HEADER_KEY_NAME = "Ocp-Apim-Subscription-Key";
    static final String GEOCLIENT_KEY_ENV_VARIABLE = "GEOCLIENT_KEY";
    static final String GEOCLIENT_SEARCH_ENDPOINT = "https://api.nyc.gov/geoclient/v2/search";

    private final String subscriptionKey;

    public App(String subscriptionKey) {
        this.subscriptionKey = subscriptionKey;
        if(this.subscriptionKey == null) {
            throw new IllegalArgumentException("subscriptionKey cannot be null.");
        }
    }

    public String geocode(String location) {

        HttpClient client = HttpClient.newHttpClient();

        // Encode the location parameter in case it contains special characters
        String locationParameter = URLEncoder.encode(location, StandardCharsets.UTF_8);
        // The complete URL == endpoint URL + resource (search) + query string
        // parameters (/search requires an "input" parameter)
        String searchUrl = GEOCLIENT_SEARCH_ENDPOINT + "?input=" + locationParameter;
        System.out.println("Calling /geoclient/v2 with URL: " + searchUrl);

        try {
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(searchUrl))
                    .header(HEADER_KEY_NAME, subscriptionKey)
                    .header("Cache-Control", "no-cache")
                    .header("Content-Type", "application/json")
                    .header("Accept", "application/json")
                    .GET()
                    .build();

            // Send the request and get the response
            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

            System.out.println("Response Code: " + response.statusCode());
            System.out.println("Response Body: " + response.body());
            HttpHeaders headers = response.headers();
            System.out.println("\nResponse Headers:");
            headers.map().forEach((k, v) -> System.out.println(k + ":" + v));

            return response.body();

        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

    public static void showUsage() {
        System.out.println("Usage: ");
    }

    public static void main(String[] args) {
        String location = null;
        String geoclientKey = null;
        switch (args.length) {
            case 1:
                location = args[0];
                geoclientKey = System.getenv(GEOCLIENT_KEY_ENV_VARIABLE);
                break;
            case 2:
                location = args[0];
                geoclientKey = args[1];
                break;
            default:
                showUsage();
                break;
        }
        if (geoclientKey == null) {
            showUsage();
            return;
        }
        System.out.println(new App(geoclientKey).geocode(location));
    }
}
