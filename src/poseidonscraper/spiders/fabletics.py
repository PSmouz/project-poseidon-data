"""Fabletics spider

This spider crawls the gymshark.com website and extracts the following
information from the product pages:

- Product Name
- Product Category
- Product Collection
- Product Rating
- Product Images
- Product Materials
- Product Sizes
- Product Color
- Product Price

Categories (default all):
    - leggings
    - underwear
    - skirts

Country (default de):
    - de
    - us

Example Usage:
    scrapy crawl gymshark -a country=de -a categories=leggings,skorts

"""
import json
import re
import math
import uuid

import scrapy
from scrapy.http import Request
from scrapy.loader import ItemLoader

from ..items import AlphaleteItem

# TODO: The have bot protection, so we need to bypass it


class FableticsSpider(scrapy.Spider):
    name = "fabletics"
    allowed_domains = ["fabletics.com"]

    def __init__(self, categories=None, country="us", *args, **kwargs):
        super(FableticsSpider, self).__init__(*args, **kwargs)

        # Select Category from CL Argument
        if categories is None:
            categories = ["leggings", "underwear", "skirts"]
        else:
            categories = categories.split(",")

        categories_map = {
            "leggings": "leggings/",
            "underwear": "underwear/",
            "skirts": "dresses-skirts/",
        }

        # self.start_urls = [
        #     f"https://{self.allowed_domains[0]}/collections/womens"
        #     f"-{categories_map[cat]}"
        #     for cat in categories
        # ]
        self.start_urls = ["https://www.fabletics.com/api/graphql"]

    # def parse(self, response):
    #     """
    #
    #     Args:
    #         response:
    #     """
    #     scope = response.url.split("/")[-2].replace("womens-", "")
    #     scope_map = {
    #         "leggings": "436180492",
    #         "underwear": "68415258742",
    #         "dresses-skirts": "289912881336",
    #     }
    #
    #     pattern = r"collection_count:\s*(\d+)"
    #     matches = re.search(pattern, response.text)
    #     products_amount = matches.group(1)
    #
    #     for i in range(math.ceil(int(products_amount) / 50)):
    #         products_url = (
    #             f"https://premium-alphalete.mybcapps.com/bc-sf-filter"
    #             f"/filter?shop=alphaleteathletics.myshopify.com&limit="
    #             f"50&product_available=false&variant_available=false"
    #             f"&build_filter_tree=true&check_cache=true&pg="
    #             f"collection_page&event_type=collection&page="
    #             f"{str(i + 1)}&sort="
    #             f"manual&collection_scope={scope_map[scope]}"
    #         )
    #
    #         yield Request(products_url, callback=self.parse_products)

    def parse(self, response):
        headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9,de-DE;q=0.8,de;q=0.7,la;q=0.6,ar;q=0.5",
            "apollographql-client-name": "@techstyle/shapewear-react Web SPA",
            "apollographql-client-version": "1.0.0-stg.2606-2606 Web Browser",
            "content-type": "application/json",
            "sec-ch-ua": '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "true-client-ip": "141.70.45.23",
            "x-api-key": "HprFg79PZk8K7GjkCSAyqikIdqXCE5V4dNuk8njc",
            "x-tfg-cacheby": "default:compute",
            "x-tfg-storedomain": "www.fabletics.com",
            "Referer": "https://www.fabletics.com/products/SEAMLESS-ULTRA-HW-SPORT-STRIPE-78-LEGGING-LG2357486-0707?psrc=womens_bottoms_leggings",
            "Referrer-Policy": "strict-origin-when-cross-origin",
        }

        payload = {
            "operationName": "ProductByPermalink",
            "variables": {
                "withWarehouseInv": False,
                "useRetailPriceForDiscount": True,
                "includeSwatchType": True,
                "permalink": "SEAMLESS-ULTRA-HW-SPORT-STRIPE-78-LEGGING-LG2357486-0707",
                "fetchRelatedProducts": True,
            },
            "query": """
                fragment IndividualProductMainParts on IndividualProduct {
                  permalink
                  masterProductId
                  groupCode
                  label: title
                  type
                  productTypeId: typeId
                  isWaitlistEligible
                  productCategoryIdList: categoryIds
                  wearItWithProductIds
                  featuredProductLocationIdList
                  tagIdList: tagIds
                  dateExpected
                  description
                  metadata {
                    description
                    title
                    __typename
                  }
                  isAvailable
                  __typename
                }

                fragment IndividualProductPriceParts on IndividualProduct {
                  retailUnitPrice: regularPrice
                  defaultUnitPrice: vipPrice
                  saleUnitPrice: salePrice
                  tokenRedemptionValue
                  __typename
                }

                fragment ProductImageSetParts on ImageSet {
                  images {
                    angle
                    sizes {
                      height
                      width
                      url
                      __typename
                    }
                    __typename
                  }
                  model {
                    firstName
                    lastName
                    heightInInches
                    id
                    braSize
                    topSize
                    bottomSize
                    __typename
                  }
                  __typename
                }

                fragment IndividualProductImagesParts on IndividualProduct {
                  imageSets {
                    default {
                      ...ProductImageSetParts
                      __typename
                    }
                    plus {
                      ...ProductImageSetParts
                      __typename
                    }
                    memberModels {
                      ...ProductImageSetParts
                      __typename
                    }
                    __typename
                  }
                  __typename
                }

                fragment IndividualProductVideoParts on IndividualProduct {
                  video {
                    url
                    source
                    sourceId
                    __typename
                  }
                  __typename
                }

                fragment IndividualProductReviewSummaryParts on IndividualProduct {
                  reviewCount
                  averageReview
                  __typename
                }

                fragment IndividualProductSelectorsParts on IndividualProduct {
                  swatches {
                    color
                    url
                    __typename
                  }
                  attributes {
                    label
                    field
                    options {
                      label
                      value
                      alias
                      __typename
                    }
                    __typename
                  }
                  skus {
                    requiredUserStatus
                    dateAvailablePreorder
                    masterProductId
                    productId
                    availableQuantity
                    isPreorder
                    permalink
                    options {
                      attribute
                      value
                      __typename
                    }
                    __typename
                  }
                  __typename
                }

                fragment IndividualProductAllPreloadParts on IndividualProduct {
                  ...IndividualProductMainParts
                  ...IndividualProductPriceParts
                  ...IndividualProductImagesParts
                  ...IndividualProductVideoParts
                  ...IndividualProductReviewSummaryParts
                  ...IndividualProductSelectorsParts
                  __typename
                }

                fragment BundleProductMainParts on BundleProduct {
                  label: title
                  masterProductId
                  permalink
                  wearItWithProductIds
                  featuredProductLocationIdList
                  productTypeId: typeId
                  dateExpected
                  tagIdList: tagIds
                  description
                  metadata {
                    description
                    title
                    __typename
                  }
                  __typename
                }

                fragment BundleProductImagesParts on BundleProduct {
                  imageSets {
                    default {
                      ...ProductImageSetParts
                      __typename
                    }
                    plus {
                      ...ProductImageSetParts
                      __typename
                    }
                    memberModels {
                      ...ProductImageSetParts
                      __typename
                    }
                    __typename
                  }
                  __typename
                }

                fragment BundleProductVideoParts on BundleProduct {
                  video {
                    url
                    source
                    sourceId
                    __typename
                  }
                  __typename
                }

                fragment BundleProductPriceParts on BundleProduct {
                  retailUnitPrice: regularPrice
                  defaultUnitPrice: vipPrice
                  saleUnitPrice: salePrice
                  tokenRedemptionValue
                  __typename
                }

                fragment BundleProductReviewSummaryParts on BundleProduct {
                  reviewCount
                  averageReview
                  __typename
                }

                fragment BundleProductAllPreloadParts on BundleProduct {
                  ...BundleProductMainParts
                  ...BundleProductImagesParts
                  ...BundleProductVideoParts
                  ...BundleProductPriceParts
                  ...BundleProductReviewSummaryParts
                  __typename
                }

                query ProductByPermalink($permalink: String, $fetchRelatedProducts: Boolean, $withWarehouseInv: Boolean! = false, $useRetailPriceForDiscount: Boolean! = false, $includeSwatchType: Boolean! = false, $excludeSkus: [String!], $gridGender: String) {
                  product: productByPermalink(
                    permalink: $permalink
                    fetchRelatedProducts: $fetchRelatedProducts
                    useRetailPriceForDiscount: $useRetailPriceForDiscount
                    includeSwatchType: $includeSwatchType
                    excludeSkus: $excludeSkus
                    gridGender: $gridGender
                  ) {
                    ... on IndividualProduct {
                      ...IndividualProductAllPreloadParts
                      isAvailable
                      membershipBrandId
                      requiredUserStatus
                      styleCode
                      styleLabel
                      skus {
                        warehouseInventory @include(if: $withWarehouseInv) {
                          id
                          quantity
                          __typename
                        }
                        itemNumber
                        availableQuantityPreorder
                        swatchType @include(if: $includeSwatchType)
                        __typename
                      }
                      description
                      defaultCategoryLabel
                      details {
                        fabricContent
                        fabricType
                        features
                        fabricTagId
                        __typename
                      }
                      metadata {
                        description
                        title
                        __typename
                      }
                      associatedBundleProductIdsList
                      alias
                      itemNumber
                      styleCode
                      styleLabel
                      personalizations {
                        productId
                        templateLabel
                        type
                        customizationTemplateId
                        customizationTypeId
                        locations {
                          locationId
                          label
                          thumbnail
                          customizations {
                            customizationId
                            label
                            options {
                              optionId
                              label
                              __typename
                            }
                            __typename
                          }
                          __typename
                        }
                        unitPrice
                        promoPrice
                        __typename
                      }
                      datePreorderExpires
                      isTokenOnly
                      __typename
                    }
                    ... on BundleProduct {
                      ...BundleProductAllPreloadParts
                      isAvailable
                      requiredUserStatus
                      componentExclusions {
                        sku
                        __typename
                      }
                      bundleComponentProducts {
                        ...IndividualProductAllPreloadParts
                        description
                        defaultCategoryLabel
                        details {
                          fabricContent
                          fabricType
                          features
                          fabricTagId
                          __typename
                        }
                        associatedBundleProductIdsList
                        skus {
                          itemNumber
                          availableQuantityPreorder
                          swatchType @include(if: $includeSwatchType)
                          __typename
                        }
                        styleCode
                        styleLabel
                        personalizations {
                          productId
                          templateLabel
                          type
                          customizationTemplateId
                          customizationTypeId
                          locations {
                            locationId
                            label
                            thumbnail
                            customizations {
                              customizationId
                              label
                              options {
                                optionId
                                label
                                __typename
                              }
                              __typename
                            }
                            __typename
                          }
                          unitPrice
                          promoPrice
                          __typename
                        }
                        __typename
                      }
                      description
                      alias
                      itemNumber
                      metadata {
                        description
                        title
                        __typename
                      }
                      tokenRedemptionValue
                      isTokenOnly
                      __typename
                    }
                    __typename
                  }
                  __typename
                }
            """,
        }

        yield scrapy.http.JsonRequest(
            url=self.start_urls[0],
            method="POST",
            headers=headers,
            body=json.dumps(payload),
            callback=self.parse_result,
        )

    def parse_result(self, response):
        data = json.loads(response.text)
        # Handle the response data as needed
        # Example: Extract product details from the response
        product_details = data.get("data", {}).get("product", {})
        self.log(product_details)

    def parse_products(self, response):
        """

        Args:
            response:
        """
        products = json.loads(response.text)["products"]

        for product in products:
            item_url = (
                f"https://alphaleteathletics.com/search?view=json&type"
                f"=product&sort_by=created-descending&q=title%3A"
                f"{product['title'].replace(' ', '%20')}"
                f"%20AND%20product_type%3A"
                f"{product['product_type'].replace(' ', '%20')}"
            )
            yield Request(
                item_url,
                callback=self.parse_item,
                meta={"original_url": response.url},
            )

    def parse_item(self, response):
        """

        Args:
            response:
        """
        product = json.loads(response.text)[0]

        name, color = self.parse_title(product["title"])
        url = f"https://{self.allowed_domains[0]}/products/{product['handle']}"

        sizes = [
            {"size": size["title"], "quantity": size["inventory_quantity"]}
            for size in product["variants"]
        ]

        loader = ItemLoader(item=AlphaleteItem(), response=response)
        loader.add_value("url", url)
        loader.add_value("id", str(uuid.uuid4()))
        loader.add_value("name", name)
        loader.add_value("category_name", self.get_category(name))
        loader.add_value("collection_name", self.get_collection(name))
        loader.add_value(
            "images", ["https:" + image for image in product["images"]]
        )
        loader.add_value("materials", product["description"])
        loader.add_value("sizes", sizes)
        loader.add_value("color", color)
        loader.add_value("price", product["price"])
        loader.add_value("price", product["compare_at_price"])

        yield loader.load_item()
