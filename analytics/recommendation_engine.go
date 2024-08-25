package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"math"
	"net/http"
	"os"
)

type Product struct {
	ID    string  `json:"id"`
	Name  string  `json:"name"`
	Score float64 `json:"score"`
}

func LoadEnvironmentVariables() {
	os.Setenv("PRODUCTS_API", "https://example.com/api/products")
}

func FetchProducts(apiURL string) ([]Product, error) {
	resp, err := http.Get(apiURL)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	var products []Product
	err = json.Unmarshal(body, &products)
	if err != nil {
		return nil, err
	}

	return products, nil
}

func CalculateRecommendationScores(products []Product) []Product {
	for i := range products {
		products[i].Score = 1.0 / (1.0 + math.Exp(-float64(i)))
	}
	return products
}

func RecommendProducts(products []Product, topN int) []Product {
	CalculateRecommendationScores(products)

	for i := 0; i < len(products); i++ {
		for j := 0; j < len(products)-i-1; j++ {
			if products[j].Score < products[j+1].Score {
				products[j], products[j+1] = products[j+1], products[j]
			}
		}
	}

	if topN > len(products) {
		topN = len(products)
	}
	return products[:topN]
}

func main() {
	LoadEnvironmentVariables()

	apiURL := os.Getenv("PRODUCTS_API")
	if apiURL == "" {
		fmt.Println("PRODUCTS_API environment variable is not set.")
		return
	}

	products, err := FetchProducts(apiURL)
	if err != nil {
		fmt.Printf("Error fetching products: %s\n", err)
		return
	}

	topProducts := RecommendProducts(products, 5)
	fmt.Println("Top recommended products:")
	for _, product := range topProducts {
		fmt.Printf("ID: %s, Name: %s, Score: %.2f\n", product.ID, product.Name, product.Score)
	}
}