import { SelectField } from '@/components/form-elements/SelectField';
import { useFetchByFormat } from '@/features/study-progress/api/fetch-study-progress/useFetchByFormat';
import { useFetchBySubject } from '@/features/study-progress/api/fetch-study-progress/useFetchBySubject';
import { useFetchScoreByFormat } from '@/features/study-progress/api/fetch-study-progress/useFetchScoreByFormat';
import { useFetchScoreBySubject } from '@/features/study-progress/api/fetch-study-progress/useFetchScoreBySubject';
import {
  AggregateTarget,
  TimeLimitWindow,
} from '@/features/study-progress/types/constants';
import { replaceUnderscore, titleString } from '@/utils/format-string';
import { useForm, useWatch } from 'react-hook-form';

export const StudyProgressSummarization = () => {
  const { register, control } = useForm<{ limit: TimeLimitWindow }>({
    defaultValues: { limit: TimeLimitWindow.All },
  });

  let days: number;
  let months: number;
  let years: number;

  const timeLimitWindow = useWatch({ control, name: 'limit' });

  switch (timeLimitWindow) {
    case TimeLimitWindow.All:
      days = 0;
      months = 0;
      years = 0;
      break;

    case TimeLimitWindow.Week:
      days = 7;
      months = 0;
      years = 0;
      break;

    case TimeLimitWindow.Month:
      days = 0;
      months = 1;
      years = 0;
      break;

    case TimeLimitWindow.Year:
      days = 0;
      months = 0;
      years = 1;
      break;
  }

  // By format
  const fetchActivitiesByFormat = useFetchByFormat(
    AggregateTarget.CountActivity,
    days,
    months,
    years,
  );
  const fetchItemsByFormat = useFetchByFormat(
    AggregateTarget.CountItem,
    days,
    months,
    years,
  );
  const fetchScoresByFormat = useFetchScoreByFormat(days, months, years);

  // By subject
  const fetchActivitiesBySubject = useFetchBySubject(
    AggregateTarget.CountActivity,
    days,
    months,
    years,
  );
  const fetchItemsBySubject = useFetchBySubject(
    AggregateTarget.CountItem,
    days,
    months,
    years,
  );
  const fetchScoresBySubject = useFetchScoreBySubject(days, months, years);

  const hookList = [
    fetchActivitiesByFormat,
    fetchItemsByFormat,
    fetchScoresByFormat,
    fetchActivitiesBySubject,
    fetchItemsBySubject,
    fetchScoresBySubject,
  ];

  // Extracted information
  const totalActivities = Object.values(
    fetchActivitiesByFormat.data ?? {},
  ).reduce((sum, count) => sum + count, 0);
  const totalItems = Object.values(fetchItemsByFormat.data ?? {}).reduce(
    (sum, count) => sum + count,
    0,
  );
  const totalUserScore = Object.values(fetchScoresByFormat.data ?? {}).reduce(
    (sum, scores) => sum + scores[0],
    0,
  );
  const totalMaximumScore = Object.values(
    fetchScoresByFormat.data ?? {},
  ).reduce((sum, scores) => sum + scores[1], 0);

  return (
    <div>
      <SelectField
        label="Statistics range:"
        name="limit"
        labelStyle="font-semibold text-xl mr-5"
        inputStyle="w-1/5 select-primary"
        options={Object.entries(TimeLimitWindow).map(([label, value]) => {
          return {
            label: label === 'All' ? label : 'Last ' + label.toLowerCase(),
            value,
          };
        })}
        register={register}
      />

      {hookList.some((hook) => hook.isError) && <p>Failed to fetch data.</p>}
      {hookList.some((hook) => hook.isPending) && <p>Fetching data...</p>}

      {hookList.some((hook) => hook.isError || hook.isPending) || (
        <div>
          <div>
            <p className="divider font-bold text-2xl my-6">
              Total study activities generated: {totalActivities}
            </p>

            {/* Activities by format */}
            <p className="font-bold text-lg my-2">
              Study activities count grouped by format:
            </p>
            <ul className="list-disc ml-12 space-y-1">
              {Object.entries(fetchActivitiesByFormat.data ?? {}).map(
                ([format, count]) => {
                  return (
                    <li key={format}>
                      {titleString(replaceUnderscore(format))}: {count}
                    </li>
                  );
                },
              )}
            </ul>

            {/* Activities by subject */}
            <p className="font-bold text-lg my-2">
              Study activities count grouped by subject:
            </p>
            <ul className="list-disc ml-12 space-y-1">
              {Object.entries(fetchActivitiesBySubject.data ?? {}).map(
                ([subject, count]) => {
                  return (
                    <li key={subject}>
                      {titleString(replaceUnderscore(subject))}: {count}
                    </li>
                  );
                },
              )}
            </ul>
          </div>

          <div>
            <p className="divider font-bold text-2xl my-6">
              Total study activity items generated: {totalItems}
            </p>

            {/* Items by format */}
            <p className="font-bold text-lg my-2">
              Study activity items count grouped by format:
            </p>
            <ul className="list-disc ml-12 space-y-1">
              {Object.entries(fetchItemsByFormat.data ?? {}).map(
                ([format, count]) => {
                  return (
                    <li key={format}>
                      {titleString(replaceUnderscore(format))}: {count}
                    </li>
                  );
                },
              )}
            </ul>

            {/* Items by subject */}
            <p className="font-bold text-lg my-2">
              Study activity items count grouped by subject:
            </p>
            <ul className="list-disc ml-12 space-y-1">
              {Object.entries(fetchItemsBySubject.data ?? {}).map(
                ([subject, count]) => {
                  return (
                    <li key={subject}>
                      {titleString(replaceUnderscore(subject))}: {count}
                    </li>
                  );
                },
              )}
            </ul>
          </div>

          <div>
            <p className="divider font-bold text-2xl my-6">
              Exercise average grades:{' '}
              {Number.isNaN(totalUserScore / totalMaximumScore)
                ? 'No data'
                : (totalUserScore / totalMaximumScore) * 10 + ' out of 10'}{' '}
            </p>

            {/* Scores by format */}
            <p className="font-bold text-lg my-2">
              <b>Exercise average grades grouped by format:</b>
            </p>
            <ul className="list-disc ml-12 space-y-1">
              {Object.entries(fetchScoresByFormat.data ?? {}).map(
                ([format, scores]) => {
                  return (
                    <li key={format}>
                      {titleString(replaceUnderscore(format))}:{' '}
                      {Number.isNaN(scores[0] / scores[1])
                        ? 'No data'
                        : (scores[0] / scores[1]) * 10 + ' out of 10'}
                    </li>
                  );
                },
              )}
            </ul>

            {/* Scores by subject */}
            <p className="font-bold text-lg my-2">
              <b>Exercise average grades grouped by subject:</b>
            </p>
            <ul className="list-disc ml-12 space-y-1">
              {Object.entries(fetchScoresBySubject.data ?? {}).map(
                ([subject, scores]) => {
                  return (
                    <li key={subject}>
                      {titleString(replaceUnderscore(subject))}:{' '}
                      {Number.isNaN(scores[0] / scores[1])
                        ? 'No data'
                        : (scores[0] / scores[1]) * 10 + ' out of 10'}
                    </li>
                  );
                },
              )}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};
