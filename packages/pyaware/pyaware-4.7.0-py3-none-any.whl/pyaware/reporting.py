class Aggregate:
    @staticmethod
    def mean(data):
        """
        :return: mean of values stored
        """
        return sum(data) / len(data)

    @staticmethod
    def max(data):
        """
        :return: max of values
        """
        return max(data)

    @staticmethod
    def min(data):
        """
        :return: min of values
        """
        return min(data)

    @staticmethod
    def latest(data):
        """
        :return: return the latest sample read
        """
        return data[-1]

    @staticmethod
    def samples(data):
        """
        :return: number of samples
        """
        return len(data)

    @staticmethod
    def all(data):
        """
        :return: list of all values stored in form of [value ...]
        """
        return data.copy()

    @staticmethod
    def median(data):
        """
        :return: The median of the data, if there is an even number of samples then take the mean of the two median samples
        """
        data = sorted(data)
        n = len(data)
        return data[n // 2]

    @staticmethod
    def sum(data):
        """
        :return: Sum of the data provided
        """
        return sum(data)


class Report:
    """
    Store the desired aggregates and filters.
    Reports data
    Process incoming data to filter and aggregate data in
    """

    def __init__(self, *args, **kwargs):
        self._filters = []

    def _build_filter(self, aggregate, **kwargs):
        filters = {k: v for k, v in kwargs.items() if v is not None}
        filt = {"filter": filters, "aggregate": aggregate}
        return filt

    def mean(self, labels=None, not_labels=None, dev_ids=None, not_dev_ids=None):
        self._filters.append(
            self._build_filter(
                Aggregate.mean,
                labels=labels,
                not_labels=not_labels,
                dev_ids=dev_ids,
                not_dev_ids=not_dev_ids,
            )
        )

    def sum(self, labels=None, not_labels=None, dev_ids=None, not_dev_ids=None):
        self._filters.append(
            self._build_filter(
                Aggregate.sum,
                labels=labels,
                not_labels=not_labels,
                dev_ids=dev_ids,
                not_dev_ids=not_dev_ids,
            )
        )

    def max(self, labels=None, not_labels=None, dev_ids=None, not_dev_ids=None):
        self._filters.append(
            self._build_filter(
                Aggregate.max,
                labels=labels,
                not_labels=not_labels,
                dev_ids=dev_ids,
                not_dev_ids=not_dev_ids,
            )
        )

    def min(self, labels=None, not_labels=None, dev_ids=None, not_dev_ids=None):
        self._filters.append(
            self._build_filter(
                Aggregate.min,
                labels=labels,
                not_labels=not_labels,
                dev_ids=dev_ids,
                not_dev_ids=not_dev_ids,
            )
        )

    def latest(self, labels=None, not_labels=None, dev_ids=None, not_dev_ids=None):
        self._filters.append(
            self._build_filter(
                Aggregate.latest,
                labels=labels,
                not_labels=not_labels,
                dev_ids=dev_ids,
                not_dev_ids=not_dev_ids,
            )
        )

    def samples(self, labels=None, not_labels=None, dev_ids=None, not_dev_ids=None):
        self._filters.append(
            self._build_filter(
                Aggregate.samples,
                labels=labels,
                not_labels=not_labels,
                dev_ids=dev_ids,
                not_dev_ids=not_dev_ids,
            )
        )

    def all(self, labels=None, not_labels=None, dev_ids=None, not_dev_ids=None):
        self._filters.append(
            self._build_filter(
                Aggregate.all,
                labels=labels,
                not_labels=not_labels,
                dev_ids=dev_ids,
                not_dev_ids=not_dev_ids,
            )
        )

    def median(self, labels=None, not_labels=None, dev_ids=None, not_dev_ids=None):
        self._filters.append(
            self._build_filter(
                Aggregate.median,
                labels=labels,
                not_labels=not_labels,
                dev_ids=dev_ids,
                not_dev_ids=not_dev_ids,
            )
        )

    def report(self, data):
        """
        Iterate through the data (dev_id, label, data_points)
        Apply the report filters to the dev_id and label to get the appropriate aggregate functions for that datapoint
        Aggregate the data by dev_id and label in the form
        {<dev_id>:
            {
            <label>:
                {
                <agg1>: <value1>,
                <agg2>: <value2>
                }
            }
        }
        :param data:
        :return:
        """
        report_data = {}
        for dev_id, label, data_points in data:
            if len(data_points) == 0:
                continue
            aggs = self.process_aggregates(dev_id=dev_id, label=label)
            if aggs:
                if not dev_id in report_data:
                    report_data[dev_id] = {}
                report_data[dev_id][label] = {
                    agg.__name__: agg(data_points) for agg in aggs
                }
        return report_data

    def process_aggregates(self, dev_id, label):
        """
        Matches filters with the parsed in **kwargs. Filters prefixed with not_ will check that they are not in filter
        and others will check that they are in the filter. If that parameter isn't checked then it is assumed that we
        want that data
        :return: Aggregate functions which pass the filter
        """
        aggregates = set()
        for agg_filter in self._filters:
            filt = agg_filter["filter"]
            if self.process_filter(filt, dev_id, label):
                aggregates.add(agg_filter["aggregate"])
        return aggregates

    def process_filter(self, filt, dev_id, label):
        """
        Iterates through the filter_list, If any parameter matches the data provided in the **kwargs then it returns
        False, Otherwise return True
        :param filt: Filter dictionary of form {<filt_type>: <set>}
        filters implemented: labels, not_labels, dev_ids, not_dev_ids
        :return: Boolean
        """
        for filt_type, filt_set in filt.items():
            if filt_type == "labels":
                if label not in filt_set:
                    return False
            elif filt_type == "not_labels":
                if label in filt_set:
                    return False
            elif filt_type == "dev_ids":
                if dev_id not in filt_set:
                    return False
            elif filt_type == "not_dev_ids":
                if dev_id in filt_set:
                    return False
        return True


class ReportNewData(Report):
    """
    Report data since last report to the cloud
    Needs to be adapted after PYAW-15
    """

    def report(self, data):
        """
        Iterate through the data (dev_id, label, data_points)
        Apply the report filters to the dev_id and label to get the appropriate aggregate functions for that datapoint
        Aggregate the data by dev_id and label in the form
        {<dev_id>:
            {
            <label>:
                {
                <agg1>: <value1>,
                <agg2>: <value2>
                }
            }
        }
        :param data:
        :return:
        """
        report_data = {}
        for dev_id, dev_type, label, data_points in data:
            if len(data_points) == 0:
                continue
            aggs = self.process_aggregates(dev_id=dev_id, label=label)
            if aggs:
                if not dev_id in report_data:
                    report_data[dev_id] = {"device_type": dev_type, "data": {}}
                report_data[dev_id]["data"][label] = {
                    agg.__name__: agg(data_points) for agg in aggs
                }
            # Clears the existing readings so next time it will be a fresh report.
            # This needs changing going forward as there might be multiple reports relying on that data
            # Check for PYAW-15
            data_points.clear()
        return report_data


class ReportDataTimeRange(Report):
    """
    Report data between two time ranges
    Requires PYAW-15
    """


class ReportQuery(Report):
    """
    Report a complex query
    Should be used for custom queries such as returning all data for things such as time series graphing.
    Requires PYAW-15
    """
