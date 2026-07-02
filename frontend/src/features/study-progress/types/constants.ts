// ----- AGGREGATE TARGET ----- //

export const AggregateTarget = {
  CountActivity: 'COUNT_ACTIVITY',
  CountItem: 'COUNT_ITEM',
  Score: 'SCORE',
} as const;

export type AggregateTarget =
  (typeof AggregateTarget)[keyof typeof AggregateTarget];

// ----- CRITERION ----- //

export const CriterionAttribute = {
  SubjectType: 'subject_type',
  ActivityType: 'activity_type',
  ActivityFormat: 'activity_format',
  CreatedAt: 'created_at',
  SubmittedAt: 'submitted_at',
  IsSubmitted: 'is_submitted',
  InteractionId: 'interaction_id',
} as const;

export type CriterionAttribute =
  (typeof CriterionAttribute)[keyof typeof CriterionAttribute];

export const CriterionOperator = {
  Equals: 'EQ',
  NotEquals: 'NE',
  GreaterThan: 'GT',
  GreaterThanEquals: 'GE',
  LessThan: 'LT',
  LessThanEquals: 'LE',
  GroupBy: 'GROUP_BY',
};

export type CriterionOperator =
  (typeof CriterionOperator)[keyof typeof CriterionOperator];

// ----- TIME LIMIT WINDOWS ----- //

export const TimeLimitWindow = {
  Week: 'WEEK',
  Month: 'MONTH',
  Year: 'YEAR',
  All: 'ALL',
} as const;

export type TimeLimitWindow =
  (typeof TimeLimitWindow)[keyof typeof TimeLimitWindow];
