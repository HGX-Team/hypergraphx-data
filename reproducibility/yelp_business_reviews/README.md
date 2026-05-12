# yelp_business_reviews reproducibility

## Dataset
- Name: yelp_business_reviews
- Description: Yelp business reviews information where nodes correspond to businesses with meta-attributes such as business stars and location (latitude and longitude). Hyperedges correspond to users and contain the set of businesses reviewed by that user. The source listed here contains the raw data from which this hypergraph dataset is constructed. An alternative source would be 'https://www.kaggle.com/datasets/yelp-dataset/yelp-dataset'.

## Source data
- https://github.com/jianhao2016/AllSet/tree/6281a2f1a91f6f26040777bb0b2578fc035dc57a/data/raw_data

## Script
- `generate_yelp_business_reviews.py`

## Steps
1. Download or access the source data from the link above.
2. Place the raw files in a directory and pass that path as `raw_dir`.
3. Run `python reproducibility/yelp_business_reviews/generate_yelp_business_reviews.py /path/to/raw --output-dir /path/to/output`.
4. Validate the printed node/edge counts and generated file sizes.

## Output
- `yelp_business_reviews.json`
- `yelp_business_reviews.hgx`
