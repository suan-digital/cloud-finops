<!-- Source: FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec (Community Specification License 1.0) -->

# Introduction

*This section is non-normative.*

FOCUS is a standards development organization (SDO) formed to establish an open, consensus-driven standard for billing data. In the absence of a broadly adopted standard, infrastructure and service *service providers* have relied on proprietary billing schemas and inconsistent terminology, making cost data difficult to normalize and act upon across environments. This lack of conformance has forced FinOps *practitioners* to develop best-effort custom normalization schemes for each provider, in order to perform essential FinOps capabilities such as chargeback, cost allocation, budgeting and forecasting.

The FOCUS Specification, developed by a global community of practitioners and vendors, defines a consistent, vendor-neutral approach to billing data. It is designed to improve interoperability between service providers, reduce operational complexity, and enable greater transparency in cloud and SaaS cost management.

## Background and History

This project is supported by the [FinOps Foundation][FODO]. This work initially started under the Open Billing working group under the FinOps Foundation. The decision was made in Jan 2023 to begin to migrate the work to a newly formed project under the Linux Foundation called the FinOps Open Cost and Usage Specification (FOCUS) to better support the creation of a specification.

## Intended Audience

This specification is designed to be used by three major groups:

* Billing data generators: Entities that present consumption-based billing information related to infrastructure and *service providers*, such as (but not limited to):
  * Cloud Service Providers (CSPs)
  * Software as a Service (SaaS) platforms
  * Managed Service Providers (MSPs)
  * Internal infrastructure and service platforms
* FinOps tool *providers*: Organizations that provide tools to assist with FinOps
* FinOps practitioners: Organizations and individuals consuming billing data for doing FinOps

## Scope

The FOCUS working group will develop an open-source specification for billing data. The schema will define data *dimensions*, *metrics*, a set of attributes about billing data, and a common lexicon for describing billing data.

## Design Principles

The following principles were considered while building the specification.

### FOCUS is an iterative, living specification

* Incremental iterations of the specification released regularly will provide higher value to practitioners and allow feedback as the specification develops. The goal is not to get to a complete, finished specification in one pass.

### Working backward with ease of adoption

* Aim to work backward from essential FinOps capabilities that practitioners need to perform to prioritize the dimensions, metrics and attributes of the cost and usage data that should be defined in the specification to fulfill that capability.
* Be FinOps scenario-driven. Define columns that answer scenario questions; don't look for scenarios to fit a column, each column must have a use case.
* Don't add dimensions or metrics to the specification just because it can be added.
* When defining the specification, consideration should be made to existing data already in the major cloud service providers' (AWS, GCP, Azure, OCI) datasets.
* As long as it solves the FinOps use case, there should be a preference to align with data that is already present in a majority of the major data generators.
* Strive for simplicity. However, prioritize accuracy, clarity, and consistency.
* Strive to build columns that serve a single purpose, with clear and concise names and values.
* The specification should allow data to be presented free from jargon, using simple understandable terms, and be approachable.
* Naming and terms used should be carefully considered to avoid using terms for which the definition could be confused by the reader. If a term must be used which has either an unclear or multiple definitions, it should be clarified in the glossary.
* The specification should provide all of the data elements necessary for the [Capabilities][FODOFC].

### Provider-neutral approach by default

* While the schema, naming, terminology, and attributes of many service providers are reviewed during development, this specification aims to be service-provider-neutral.
* Contributors must take care to ensure the specification examines how each decision relates to each of the major cloud service providers and SaaS vendors, not favoring any single one.
* In some cases, the approach may closely resemble one or more service provider's implementations, while in other cases, the approach might be new. In all cases, the FOCUS group (community composed of FinOps practitioners, Cloud and SaaS providers and FinOps vendors) will attempt to prioritize enabling FinOps [Capabilities][FODOFC] and alignment with the FinOps [Framework][FODOF].

### Extensibility

The FOCUS Specification is designed to support evolving FinOps needs across diverse billing models and service provider types.

While the initial focus was on billing data from Cloud Service Providers (CSPs), version 1.2 introduces foundational support for Software as a Service (SaaS) platforms, including normative columns for pricing currencies, effective cost, and contracted pricing in non-monetary units such as credits or tokens.

The specification supports extensibility through structured naming conventions (e.g., x_ custom columns), conditional requirements, and a version-aware schema approach.

Future versions of FOCUS will consider including additional FinOps capabilities such as forecasting, exchange rate modeling, and anomaly detection, while continuing to support a broader range of billing and cost datasets — including internal infrastructure platforms and marketplace offerings.

## Design Notes

### Optimize for data analysis

* Optimize columns for data analysis at scale and avoid the requirement of splitting or parsing values.
* Avoid complex JSON structures when an alternative columnar structure is possible.
* Facilitate the inclusion of data necessary for a system of record for cost and usage data to consume.

### Consistency helps with clarity

* Where possible, use consistent names that will naturally create associations between related columns in the specification.
* Column naming must strictly follow the column handling requirements.
* Use established standards (e.g., ISO8601 for dates, ISO4217 for currency).

## Typographic Conventions

The keywords "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this specification are to be interpreted as described in [BCP14](https://tools.ietf.org/html/bcp14) [[RFC2119](https://tools.ietf.org/html/rfc2119)][[RFC8174](https://tools.ietf.org/html/rfc8174)] when, and only when, they appear in all capitals, as shown here.

## FOCUS Feature Level

Under each column defined in the FOCUS specification, there exists a 'Feature level' designation that describes the column as 'Mandatory', 'Conditional', or 'Optional'. Feature level is designated based on the following criteria described in the normative requirements in each column definition:

* If the existence of a column is described with MUST with no conditions of when it applies, then the feature level is designated as 'Mandatory'.
* If the existence of a column is described as MUST with conditions of when it applies, then the feature level is designated as 'Conditional'.
* If the existence of a column is described as SHOULD, then the feature level is designated as 'Recommended'.
* If the existence of a column is described as MAY, then the feature level is designated as 'Optional'.

## Conformance Checkers and Validators

Validation tools may be employed to determine conformance of data and implementations per this specification.

The FinOps Foundation maintains a validator called the [FOCUS Validator](https://github.com/finopsfoundation/focus_validator) which it uses for its own conformance assessments and serves as a reference implementation to support validation activities.

Other validation tools may be developed and made available by third parties. The FOCUS specification does not mandate the use of any particular tool, nor does it maintain a registry of available validators.

---

# Cost and Usage

The Cost and Usage dataset is the primary dataset for FOCUS cost and usage data.

The specification for the Cost and Usage dataset defines a group of columns that provide qualitative values (such as dates, resource, and service provider information) categorized as "dimensions" and quantitative values (numeric values) categorized as "metrics" that can be used for performing various [FinOps capabilities][FODOFC]. Metrics are commonly used for aggregations (sum, multiplication, averaging etc.) and statistical operations within the dataset. Dimensions are commonly used to categorize, filter, and reveal details in your data when combined with metrics. The columns are presented in alphabetical order.

## Columns

| Column                                                                        | Column Type        | Feature Level | Allows Nulls | Data Type |
| ----------------------------------------------------------------------------- | ------------------ | ------------- | ------------ | --------- |
| Allocated Method Details                           | Dimension          | Recommended   | True         | JSON      |
| Allocated Method ID                                     | Dimension          | Conditional   | True         | String    |
| Allocated Resource ID                                 | Dimension          | Conditional   | True         | String    |
| Allocated Resource Name                             | Dimension          | Conditional   | True         | String    |
| Allocated Tags                                              | Dimension          | Conditional   | True         | JSON      |
| Availability Zone                                        | Dimension          | Recommended   | True         | String    |
| Billed Cost                                                    | Metric             | Mandatory     | False        | Decimal   |
| Billing Account ID                                       | Dimension          | Mandatory     | False        | String    |
| Billing Account Name                                   | Dimension          | Mandatory     | True         | String    |
| Billing Account Type                                   | Dimension          | Conditional   | False        | String    |
| Billing Currency                                          | Dimension          | Mandatory     | False        | String    |
| Billing Period End                                       | Dimension          | Mandatory     | False        | Date/Time |
| Billing Period Start                                   | Dimension          | Mandatory     | False        | Date/Time |
| Capacity Reservation ID                             | Dimension          | Conditional   | True         | String    |
| Capacity Reservation Status                     | Dimension          | Conditional   | True         | String    |
| Charge Category                                            | Dimension          | Mandatory     | False        | String    |
| Charge Class                                                  | Dimension          | Mandatory     | True         | String    |
| Charge Description                                      | Dimension          | Mandatory     | True         | String    |
| Charge Frequency                                          | Dimension          | Recommended   | False        | String    |
| Charge Period End                                         | Dimension          | Mandatory     | False        | Date/Time |
| Charge Period Start                                     | Dimension          | Mandatory     | False        | Date/Time |
| Commitment Discount Category                   | Dimension          | Conditional   | True         | String    |
| Commitment Discount ID                               | Dimension          | Conditional   | True         | String    |
| Commitment Discount Name                           | Dimension          | Conditional   | True         | String    |
| Commitment Discount Quantity                   | Metric             | Conditional   | True         | Decimal   |
| Commitment Discount Status                       | Dimension          | Conditional   | True         | String    |
| Commitment Discount Type                           | Dimension          | Conditional   | True         | String    |
| Commitment Discount Unit                           | Dimension          | Conditional   | True         | String    |
| Consumed Quantity                                        | Metric             | Conditional   | True         | Decimal   |
| Consumed Unit                                                | Dimension          | Conditional   | True         | String    |
| Contract Applied                                          | Dimension / Metric | Conditional   | True         | JSON      |
| Contracted Cost                                            | Metric             | Mandatory     | False        | Decimal   |
| Contracted Unit Price                                 | Metric             | Conditional   | True         | Decimal   |
| Effective Cost                                              | Metric             | Mandatory     | False        | Decimal   |
| Host Provider Name                                       | Dimension          | Mandatory     | False        | String    |
| Invoice ID                                                      | Dimension          | Recommended   | True         | String    |
| Invoice Issuer Name                                     | Dimension          | Mandatory     | False        | String    |
| List Cost                                                        | Metric             | Mandatory     | False        | Decimal   |
| List Unit Price                                             | Metric             | Conditional   | True         | Decimal   |
| Pricing Category                                          | Dimension          | Conditional   | True         | String    |
| Pricing Currency                                          | Dimension          | Conditional   | True         | String    |
| Pricing Currency Contracted Unit Price | Metric             | Conditional   | True         | Decimal   |
| Pricing Currency Effective Cost              | Metric             | Conditional   | True         | Decimal   |
| Pricing Currency List Unit Price             | Metric             | Conditional   | True         | Decimal   |
| Pricing Quantity                                          | Metric             | Mandatory     | True         | Decimal   |
| Pricing Unit                                                  | Dimension          | Mandatory     | True         | String    |
| Region ID                                                        | Dimension          | Conditional   | True         | String    |
| Region Name                                                    | Dimension          | Conditional   | True         | String    |
| Resource ID                                                    | Dimension          | Conditional   | True         | String    |
| Resource Name                                                | Dimension          | Conditional   | True         | String    |
| Resource Type                                                | Dimension          | Conditional   | True         | String    |
| Service Category                                          | Dimension          | Mandatory     | False        | String    |
| Service Name                                                  | Dimension          | Mandatory     | False        | String    |
| Service Provider Name                                 | Dimension          | Mandatory     | False        | String    |
| Service Subcategory                                    | Dimension          | Recommended   | False        | String    |
| SKU ID                                                              | Dimension          | Conditional   | True         | String    |
| SKU Meter                                                        | Dimension          | Conditional   | True         | String    |
| SKU Price Details                                         | Dimension          | Conditional   | True         | JSON      |
| SKU Price ID                                                   | Dimension          | Conditional   | True         | String    |
| Sub Account ID                                               | Dimension          | Conditional   | True         | String    |
| Sub Account Name                                           | Dimension          | Conditional   | True         | String    |
| Sub Account Type                                           | Dimension          | Conditional   | True         | String    |
| Tags                                                                 | Dimension          | Conditional   | True         | JSON      |

## Relationships

The Cost and Usage dataset can be joined to the Contract Commitment dataset through the use of the Contract Commitment ID.

* In the Cost and Usage dataset, Contract Commitment ID is a property within a JSON object array provided in Contract Applied column.
* In the Contract Commitment dataset, Contract Commitment ID is a column.

| Dataset A           | Dataset A Column  | Dataset B           | Dataset B Column       |
| ------------------- | ----------------- | ------------------- | ---------------------- |
| Cost and Usage      | Contract Applied  | Contract Commitment | Contract Commitment ID |

## Requirements

CostAndUsage adheres to the following requirements:

* CostAndUsage MUST be present.
* CostAndUsage column presence MUST adhere to the following requirements:
  * CostAndUsage SHOULD include AllocatedMethodDetails when the data generator supports Data Generator-Calculated Split Cost Allocation.
  * CostAndUsage MUST include AllocatedMethodId when the data generator supports Data Generator-Calculated Split Cost Allocation.
  * CostAndUsage MUST include AllocatedResourceId when the data generator supports Data Generator-Calculated Split Cost Allocation.
  * CostAndUsage MUST include AllocatedResourceName when the data generator supports Data Generator-Calculated Split Cost Allocation.
  * CostAndUsage MUST include AllocatedTags when the service provider supports Data Generator-Calculated Split Cost Allocation.
  * CostAndUsage SHOULD include AvailabilityZone when the host provider supports deploying resources or services within an *availability zone*.
  * CostAndUsage MUST include BilledCost.
  * CostAndUsage MUST include BillingAccountId.
  * CostAndUsage MUST include BillingAccountName.
  * CostAndUsage MUST include BillingAccountType when the invoice issuer supports more than one possible BillingAccountType value.
  * CostAndUsage MUST include BillingCurrency.
  * CostAndUsage MUST include BillingPeriodEnd.
  * CostAndUsage MUST include BillingPeriodStart.
  * CostAndUsage MUST include CapacityReservationId when the service provider supports *capacity reservations*.
  * CostAndUsage MUST include CapacityReservationStatus when the service provider supports *capacity reservations*.
  * CostAndUsage MUST include ChargeCategory.
  * CostAndUsage MUST include ChargeClass.
  * CostAndUsage MUST include ChargeDescription.
  * CostAndUsage SHOULD include ChargeFrequency.
  * CostAndUsage MUST include ChargePeriodEnd.
  * CostAndUsage MUST include ChargePeriodStart.
  * CostAndUsage MUST include CommitmentDiscountCategory when the service provider supports *commitment discounts*.
  * CostAndUsage MUST include CommitmentDiscountId when the service provider supports *commitment discounts*.
  * CostAndUsage MUST include CommitmentDiscountName when the service provider supports *commitment discounts*.
  * CostAndUsage MUST include CommitmentDiscountQuantity when the service provider supports *commitment discounts*.
  * CostAndUsage MUST include CommitmentDiscountStatus when the service provider supports *commitment discounts*.
  * CostAndUsage MUST include CommitmentDiscountType when the service provider supports *commitment discounts*.
  * CostAndUsage MUST include CommitmentDiscountUnit when the service provider supports *commitment discounts*.
  * CostAndUsage MUST include ConsumedQuantity when the service provider supports the measurement of usage.
  * CostAndUsage MUST include ConsumedUnit when the service provider supports the measurement of usage.
  * CostAndUsage MUST include ContractApplied when the service provider supports *contract commitments*.
  * CostAndUsage MUST include ContractedCost.
  * CostAndUsage MUST include ContractedUnitPrice when the service provider supports negotiated pricing concepts.
  * CostAndUsage MUST include EffectiveCost.
  * CostAndUsage MUST include HostProviderName.
  * CostAndUsage SHOULD include InvoiceId.
  * CostAndUsage MUST include InvoiceIssuerName.
  * CostAndUsage MUST include ListCost.
  * CostAndUsage MUST include ListUnitPrice when the service provider publishes unit prices exclusive of discounts.
  * CostAndUsage MUST include PricingCategory when the service provider supports more than one pricing category across all *SKUs*.
  * CostAndUsage MUST include PricingCurrency when the service provider supports pricing and billing in different currencies.
  * CostAndUsage MUST include PricingCurrencyContractedUnitPrice when the service provider supports prices in virtual currency and publishes unit prices exclusive of discounts.
  * CostAndUsage MUST include PricingCurrencyEffectiveCost when the service provider supports prices in virtual currency and publishes unit prices exclusive of discounts.
  * CostAndUsage MUST include PricingCurrencyListUnitPrice when the service provider supports prices in virtual currency and publishes unit prices exclusive of discounts.
  * CostAndUsage MUST include PricingQuantity.
  * CostAndUsage MUST include PricingUnit.
  * CostAndUsage MUST include RegionId when the host provider supports deploying resources or services within a region.
  * CostAndUsage MUST include RegionName when the host provider supports deploying resources or services within a region.
  * CostAndUsage MUST include ResourceId when the service provider supports billing based on provisioned *resources*.
  * CostAndUsage MUST include ResourceName when the service provider supports billing based on provisioned resources.
  * CostAndUsage MUST include ResourceType when the service provider supports billing based on provisioned *resources* and supports assigning types to *resources*.
  * CostAndUsage MUST include ServiceCategory.
  * CostAndUsage MUST include ServiceName.
  * CostAndUsage MUST include ServiceProviderName.
  * CostAndUsage SHOULD include ServiceSubcategory.
  * CostAndUsage MUST include SkuId when the service provider supports unit pricing concepts and publishes price lists, publicly or as part of contracting.
  * CostAndUsage MUST include SkuMeter when the service provider supports unit pricing concepts and publishes *price lists*, publicly or as part of contracting.
  * CostAndUsage MUST include SkuPriceDetails when the service provider supports unit pricing concepts and publishes *price lists*, publicly or as part of contracting.
  * CostAndUsage MUST include SkuPriceId when the service provider supports unit pricing concepts and publishes *price lists*, publicly or as part of contracting.
  * CostAndUsage MUST include SubAccountId when the service provider supports a *sub account* construct.
  * CostAndUsage MUST include SubAccountName when the service provider supports a *sub account* construct.
  * CostAndUsage MUST include SubAccountType when the service provider supports more than one possible SubAccountType value.
  * CostAndUsage MUST include Tags when the data generator supports setting user or provider-defined tags.
* CostAndUsage MUST conform to ColumnHandling requirements.
* CostAndUsage MUST conform to NullHandling requirements.
* CostAndUsage MUST conform to DiscountHandling requirements.
* CostAndUsage MUST conform to InvoiceHandling requirements.
* CostAndUsage MUST conform to DataGeneratorCalculatedSplitCostAllocationHandling requirements.
* CostAndUsage MUST conform to DatasetConfiguration requirements.

## Dataset ID

CostAndUsage

## Display Name

Cost and Usage

## Description

Describes the cost and usage incurred through using or purchasing a service provider's *resources* or *services*.

## Introduced (version)

0.5

---

# Glossary

**Accrual-Based Accounting**

An accounting method used in technology cost management to record costs in the period when resources are utilized, services are delivered, or entitlements are available for or actually consumed (including unused or expired entitlements). This approach ensures that expenses are recognized in the same timeframe as the value they provide, independent of when charges are invoiced.

**Adjustment**

A charge representing a modification to billing data to account for certain events or circumstances not previously captured, or captured incorrectly. Examples include billing errors, service disruptions, or pricing changes.

**Allocated Charge**

The [charge](#glossary:charge) that was created as the result of an allocation operation. This is used in the context of [Data Generator-Calculated Split Cost Allocation](#supportedfeatures.datagenerator-calculatedsplitcostallocation) to identify the charges that were created from the [origin charge](#glossary:origin-charge) resulting from the application of Data Generator-Calculated Split Cost Allocation.

**Allocated Method**

The process or formula by which cost is being allocated from an [origin charge](#glossary:origin-charge) to produce [allocated charges](#glossary:allocated-charge). This is used in the context of [Data Generator-Calculated Split Cost Allocation](#supportedfeatures.datagenerator-calculatedsplitcostallocation) which requires documentation of the method to be provided for any and all allocated methods used. May also be colloquially referred to as allocation method.

**Amortization**

The distribution of upfront costs over time to accurately reflect the consumption or benefit derived from the associated resources or services. Amortization is valuable when the commitment [*period*](#glossary:period) extends beyond the granularity of the source report.

**Availability Zone**

A collection of geographically separated locations containing a data center or cluster of data centers. Each availability zone (AZ) should have its own power, cooling, and networking, to provide redundancy and fault tolerance.

**Billing Account**

A container for resources and/or services that are billed together in an invoice. A billing account may have sub accounts, all of whose costs are consolidated and invoiced to the billing account.

**Billing Currency**

An identifier that represents the currency that a charge for resources and/or services was billed in.

**Billing Period**

The time window that an organization receives an invoice for, inclusive of the start date and exclusive of the end date. It is independent of the time of usage and consumption of resources and services.

**Block Pricing**

A pricing approach where the cost of a particular resource or service is determined based on predefined quantities or tiers of usage. In these scenarios, the Pricing Unit and the corresponding Pricing Quantity can be different from the Consumed Unit and Consumed Quantity.

**Cash-Based Accounting**

An accounting method used in technology cost management to record costs in the period when charges are invoiced. This approach aligns expenses with billing cycles, independent of when resources are utilized, services are delivered, or entitlements are available for or actually consumed (including unused or expired entitlements).

**Capacity Reservation**

A capacity reservation is an agreement that secures a dedicated amount of resources or services for a specified period. This ensures the reserved capacity is always available and accessible, even if it's not fully utilized. Customers are typically charged for the reserved capacity, regardless of actual consumption.

**Charge**

A row in a FOCUS-compatible cost and usage dataset.

**Charge Period**

The time window for which a charge is effective, inclusive of the start date and exclusive of the end date. The charge period for continuous usage should match the time granularity of the dataset (e.g., 1 hour for hourly, 1 day for daily). The charge period for a non-usage charge with time boundaries should match the period of eligibility.

**Cloud Service Provider (CSP)**

A company or organization that provides remote access to computing resources, infrastructure, or applications for a fee.

**Commitment**

A customer's agreement to either spend a defined monetary amount or consume a specific quantity of resources or services over a specified [*period*](#glossary:period).

**Commitment Discount**

A billing discount model that offers reduced rates on preselected SKUs in exchange for an obligated usage or spend amount over a specified [*period*](#glossary:period).  Commitment discount purchases, made upfront and/or with recurring monthly payments are amortized evenly across predefined charge periods (i.e., hourly), and unused amounts cannot be carried over to subsequent charge periods. Commitment discounts are publicly available to customers without special contract arrangements.

**Commitment Discount Flexibility**

A feature of [*commitment discounts*](#glossary:commitment-discount) that may further transform the predetermined amount of usage purchased or consumed based on additional, service-provider-specific requirements.

**Contract**

A collection of agreed terms between a service provider and a customer.

**Contract Commitment**

A specific term within a [*contract*](#glossary:contract) that defines a measurable obligation agreed upon by a provider and a customer, such as a minimum spend or usage over an agreed period of time.

**Contracted Unit Price**

The agreed-upon unit price for a single [Pricing Unit](#datasets.costandusage.pricingunit) of the associated SKU, inclusive of negotiated discounts, if present, and exclusive of any other discounts. This price is denominated in the [Billing Currency](#glossary:billing-currency).

**Correction**

A charge to correct cost or usage data in a previously invoiced [*billing period*](#glossary:billing-period).

**Credit**

A financial incentive or allowance granted by a service provider unrelated to other past/current/future charges.

**Dataset Artifact**

An abbreviated term for [*dataset instance artifact*](#glossary:dataset-instance-artifact).

**Dataset Instance**

A specific implementation of a [*FOCUS dataset*](#glossary:FOCUS-dataset) provided by a [data generator](#metadata.datagenerator). A Data Generator may provide multiple dataset instances of the same *FOCUS dataset*, each with different properties such as time granularity or differing custom column inclusions.  For example, the same 'FOCUS Cost and Usage' *FOCUS dataset* may be provided at an hourly or daily time granularity by a Data Generator. Each would be a distinct Dataset Instance.

**Dataset Instance Artifact**

A physical representation of a specific [*dataset instance*](#glossary:dataset-instance) delivered by a [data generator](#metadata.datagenerator).

**Dimension**

A specification-defined categorical attribute that provides context or categorization to billing data.

**Exclusive End Bound**

A Date/Time Format value that is not contained within the ending bound of a time period.

**Finalized Tag**

A tag with one tag value chosen from a set of possible tag values after being processed by a set of service-provider-defined or user-defined rules.

**FinOps Cost and Usage Specification (FOCUS)**

An open-source specification that defines requirements for billing data.

**FOCUS Dataset**

A structured collection of columns that conforms to the BCP14 criteria established by FOCUS. All columns included must be defined in the FOCUS Columns section of the specification.

In addition to these standardized columns, [data generators](#metadata.datagenerator) may include custom columns (prefixed with `x_`) where additional context is needed beyond what is captured in the defined FOCUS columns. If custom columns introduce record-splitting (i.e., a single original charge results in multiple rows), the data generator is responsible for ensuring that all cost and quantity metrics still meet the aggregation and consistency rules required by the specification.

The collection of datasets are designed to provide billing insight, additional context, metadata, mapping, or enrichment information that enhances the interpretability or completeness.

**Inclusive Start Bound**

A Date/Time Format value that is contained within the beginning bound of a time period.

**Interruptible**

A category of compute resources that can be paused or terminated by the CSP within certain criteria, often advertised at reduced unit pricing when compared to the equivalent non-interruptible resource.

**JSON**

A common acronym for JavaScript Object Notation, a data format codified in [ECMA-404](https://ecma-international.org/wp-content/uploads/ECMA-404_2nd_edition_december_2017.pdf) as a standard for human-readable, serializable data objects. This data format is used in FOCUS to communicate multiple pieces of information about a charge (tags, properties, etc.) in a single column.

**List Unit Price**

The suggested service-provider-published unit price for a single [Pricing Unit](#datasets.costandusage.pricingunit) of the associated [SKU](#glossary:sku), exclusive of any discounts. This price is denominated in the [Billing Currency](#glossary:billing-currency).

**Managed Service Provider (MSP)**

A company or organization that provides outsourced management and support of a range of IT services, such as network infrastructure, cybersecurity, cloud computing, and more.

**Metric**

A FOCUS-defined column that provides numeric values, allowing for aggregation operations such as arithmetic operations (sum, multiplication, averaging etc.) and statistical operations.

**National Currency**

A government-issued currency (e.g., US dollars, Euros).

**Negotiated Discount**

A contractual agreement where a customer commits to specific spend or usage goals over a specified [*period*](#glossary:period) in exchange for discounted rates across varying SKUs.  Unlike [*commitment discounts*](#glossary:commitment-discount), negotiated discounts are typically more customized to customer's accounts, can be utilized at varying frequencies, and may overlap with *commitment discounts*.

**On-Demand**

A service that is available and provided immediately or as needed, without requiring a pre-scheduled appointment or prior arrangement. In cloud computing, virtual machines can be created and terminated as needed, i.e., on demand.

**Origin Charge**

The [charge](#glossary:charge) that existed prior to an operation. This is used in the context of [Data Generator-Calculated Split Cost Allocation](#supportedfeatures.datagenerator-calculatedsplitcostallocation) to identify the charge that existed prior to the application of Data Generator-Calculated Split Cost Allocation to produce [allocated charges](#glossary:allocated-charge).

**Pascal Case**

Pascal Case (PascalCase, also known as UpperCamelCase) is a format for identifiers which contain one or more words meaning the words are concatenated together with no delimiter and the first letter of each word is capitalized.

**Period**

A time window, with a specifically defined start and end date/time.

**Potato**

A long and often painful conversation had by the FOCUS contributors. Sometimes the name of a thing that we could not yet name. No starchy root vegetables were harmed during the production of this specification. We thank potato for its contribution in the creation of this specification.

**Practitioner**

An individual who performs FinOps within an organization to maximize the business value of using cloud and cloud-like services.

**Price List**

A comprehensive list of prices offered by a service provider.

**Service Provider**

An entity that provides the [*resources*](#glossary:resource) or [*services*](#glossary:service) available for usage or purchase.

**Refund**

A return of funds that have previously been charged.

**Resource**

A unique component that incurs a charge.

**Row**

A row in a FOCUS-compatible cost and usage dataset.

**Service**

An offering that can be purchased from a service provider, and can include many types of usage or other charges; eg., a cloud database service may include compute, storage, and networking charges.

**SKU**

A construct composed of the common properties of a product offering associated with one or many SKU Prices.

**SKU Price**

A pricing construct that encompasses SKU properties (e.g., functionality and technical specifications), along with core stable pricing details for a particular SKU, while excluding dynamic or negotiable pricing elements such as unit price amounts, currency (and related exchange rates), temporal validity (e.g., effective dates), and contract- or negotiation-specific factors (e.g., contract or account identifiers, and negotiable discounts).

**Sub Account**

A sub account is an optional service-provider-supported construct for organizing resources and/or services connected to a billing account. Sub accounts must be associated with a billing account as they do not receive invoices.

**Tag**

A metadata label assigned to a resource to provide information about it or to categorize it for organizational and management purposes.

**Tag Source**

A Resource or Service-Provider-defined construct for grouping resources and/or other Service-Provider-defined construct that a Tag can be assigned to.

**Term**

An agreement specified on a [*contract*](#glossary:contract).

**Virtual Currency**

A proprietary currency (e.g., credits, tokens) issued by service providers and independent of government regulation.
