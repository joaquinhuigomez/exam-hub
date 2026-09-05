# SAA-C03 Content Spec (shared by all content agents)

Exam: AWS Certified Solutions Architect – Associate (SAA-C03). 65 questions (50 scored + 15 unscored), 130 min, pass 720/1000, $150. Formats: single-choice (4 options, 1 correct) and multiple-response (5 options, 2 correct — stem MUST say "Choose two").

Learner: Joaquin — intelligent, ADHD, already holds AWS Cloud Practitioner + AWS GenAI Developer Professional, ~50% conversant. Learns by DOING: scenario → decide → see WHY every option is right/wrong. Hates passive repetition. Wants mnemonics, decision rules, "pick the service" contrasts, numbers/limits that get tested.

## Domains and weights
- D1 Design Secure Architectures — 30%
- D2 Design Resilient Architectures — 26%
- D3 Design High-Performing Architectures — 24%
- D4 Design Cost-Optimized Architectures — 20%

## Quality bar (AWS exam style — non-negotiable)
- Scenario-based. 2–4 sentences of realistic context (company, workload, constraint) then a stem with the discriminating requirement phrase: "MOST cost-effective", "LEAST operational overhead", "MOST secure", "highest availability", "lowest latency", "minimal changes to the application".
- All distractors plausible: real AWS services that a half-prepared candidate would pick. No joke options.
- Exactly one discriminating fact separates the correct answer. Name that fact in `knowledge_point`.
- Every option's `why` must teach: state the fact that makes it right or wrong (not "this is incorrect"). 1–2 sentences each.
- `trap_alert`: the specific misread or wrong-heuristic that makes people miss this question.
- Cover the domain's task statements MECE — no two questions testing the same fact from the same angle. Vary services. Include the high-frequency comparisons the community reports: S3 storage classes & lifecycle, EBS vs EFS vs FSx (Lustre / Windows / ONTAP), RDS Multi-AZ vs read replicas vs Aurora Global, DynamoDB (DAX, global tables, on-demand vs provisioned, TTL, streams), ElastiCache Redis vs Memcached, SQS standard vs FIFO vs SNS vs EventBridge vs Kinesis (Streams vs Firehose), Route 53 routing policies, ALB vs NLB vs GWLB, CloudFront vs Global Accelerator, Direct Connect vs Site-to-Site VPN vs Transit Gateway vs peering vs PrivateLink, gateway vs interface VPC endpoints, NAT gateway vs NAT instance, SG vs NACL, IAM policy types (identity/resource/permission boundary/SCP/session), KMS key types (AWS-owned / AWS-managed / customer-managed, CloudHSM), S3 encryption modes (SSE-S3 / SSE-KMS / SSE-C / DSSE / client-side), Secrets Manager vs Parameter Store, Cognito user pools vs identity pools, WAF vs Shield vs GuardDuty vs Inspector vs Macie vs Detective vs Security Hub, Storage Gateway (File / Volume cached & stored / Tape), Snow family, DataSync vs Transfer Family vs DMS, Glue vs EMR vs Athena vs Redshift Spectrum, DR strategies (backup-restore / pilot light / warm standby / multi-site) with RPO/RTO, ASG policies (target tracking / step / scheduled / predictive), placement groups (cluster / spread / partition), EC2 purchasing (On-Demand / RI standard vs convertible / Savings Plans compute vs EC2 instance / Spot / Dedicated Host vs Instance / Capacity Reservations), Lambda limits (15 min, 10 GB memory, 10 GB ephemeral, 6 MB sync payload), Step Functions Standard vs Express, API Gateway REST vs HTTP vs WebSocket, ECS Fargate vs EC2 launch type, EKS, Organizations SCP & consolidated billing, Control Tower, Config vs CloudTrail vs CloudWatch, Compute Optimizer, Trusted Advisor, Cost Explorer vs Budgets vs CUR, S3 Transfer Acceleration, S3 Object Lock (governance vs compliance), Glacier retrieval tiers (Expedited 1–5 min / Standard 3–5 h / Bulk 5–12 h; Deep Archive 12 h / 48 h), EBS types (gp3 3000 IOPS baseline; io2 Block Express 256k IOPS; st1/sc1 throughput HDD), EFS storage classes & performance modes, instance store ephemeral, AWS Backup, Aurora Serverless v2, RDS Proxy, Redshift RA3, Kinesis shard limits (1 MB/s in, 2 MB/s out per shard), SQS limits (256 KB, 14-day retention, visibility timeout, DLQ, long polling), SNS fan-out, EventBridge schedules/rules/archive-replay, CloudFront OAC, signed URLs/cookies, field-level encryption, Lambda@Edge vs CloudFront Functions, Route 53 health checks + failover, Global Accelerator static anycast IPs, VPC Flow Logs, Network Firewall, Firewall Manager, IAM Access Analyzer, IAM Identity Center, STS AssumeRole / federation / SAML / OIDC, IMDSv2, Systems Manager Session Manager (no SSH/bastion), Macie PII, Amazon Inspector, AWS Artifact, Certificate Manager, CloudHSM FIPS 140-2 L3.

## Question JSON schema (write EXACTLY this shape; validate with python3 -m json.tool before finishing)
```json
{
  "domain": "D1",
  "title": "Design Secure Architectures",
  "questions": [
    {
      "id": "D1-Q001",
      "type": "single_choice",              // or "multiple_response"
      "difficulty": "easy|medium|hard",
      "tags": ["iam", "scp", "organizations"],
      "scenario": "A company ... (2–4 sentences)",
      "stem": "Which solution meets these requirements with the LEAST operational overhead?",
      "options": [
        {"letter": "A", "text": "...", "correct": false, "why": "..."},
        {"letter": "B", "text": "...", "correct": true,  "why": "..."},
        {"letter": "C", "text": "...", "correct": false, "why": "..."},
        {"letter": "D", "text": "...", "correct": false, "why": "..."}
      ],
      "knowledge_point": "The single discriminating fact, stated as a reusable rule.",
      "trap_alert": "The specific misread that costs points here.",
      "mnemonic": "Optional. Short memory hook if one exists.",
      "doc_refs": ["https://docs.aws.amazon.com/..."]
    }
  ]
}
```
- IDs zero-padded, sequential.
- Difficulty mix per domain: ~25% easy, ~50% medium, ~25% hard.
- ~20% multiple_response (5 options, exactly 2 correct).
- Use `\"` escaping properly; no trailing commas; no comments in the actual file.
