import sys
import re
import collections
from .FriendlyArgumentParser import FriendlyArgumentParser
from .Schedule import TimeSpecification

class AgendaParser():
	_LINE_RE = re.compile(r"\s*(?P<relspec>\*)?(?P<timespec>[^\s]+)\s+(?P<text>.*)")
	_Item = collections.namedtuple("Item", [ "rel_value", "abs_value", "text" ])

	def __init__(self, args):
		self._args = args
		self._begin_time = TimeSpecification.parse(abs_string = args.begin_time)
		self._end_time = TimeSpecification.parse(abs_string = args.end_time)
		self._abs_sum = 0
		self._rel_sum = 0
		self._items = [ ]
		self._parse_file(self._args.filename)

	def _parse_line(self, line):
		result = self._LINE_RE.fullmatch(line)
		if not result:
			raise Exception("Cannot parse: '%s'" % (line))
		result = result.groupdict()
		if result["relspec"] is not None:
			rel_value = float(result["timespec"])
			self._rel_sum += rel_value
			item = self._Item(rel_value = rel_value, abs_value = None, text = result["text"])
		else:
			abs_string = result["timespec"]
			if abs_string.isdigit():
				abs_string += " sec"
			abs_value = TimeSpecification.parse(abs_string = abs_string)
			self._abs_sum += abs_value.value
			item = self._Item(rel_value = None, abs_value = abs_value, text = result["text"])
		self._items.append(item)

	def _parse_file(self, filename):
		with open(filename) as f:
			for (lineno, line) in enumerate(f, 1):
				line = line.rstrip("\r\n")
				if line.startswith("#"):
					continue
				try:
					self._parse_line(line)
				except:
					print("Parse error in line %d:" % (lineno), file = sys.stderr)
					raise

	def dump(self):
		total_time = self._end_time.value - self._begin_time.value
		if total_time <= 0:
			raise Exception("Total time is negative or zero.")

		if self._abs_sum > total_time:
			raise Exception("More absolute time (%d minutes) allocated than in presentation (%d minutes)." % (self._abs_sum, total_time))

		rel_time = total_time - self._abs_sum
		if (rel_time > 0) and (self._rel_sum == 0):
			raise Exception("Time left in presentation (%d minutes) and no relative portion used." % (rel_time))

		rel_time_left = rel_time
		rel_pts_left = self._rel_sum
		current_time = self._begin_time.value
		for item in self._items:
			if item.rel_value is not None:
				if abs(item.rel_value - rel_pts_left) > 0.01:
					this_time = (item.rel_value / self._rel_sum) * rel_time
					this_time = round(this_time / self._args.round_mins) * self._args.round_mins
					rel_pts_left -= item.rel_value
					rel_time_left -= this_time
				else:
					this_time = round(rel_time_left / self._args.round_mins) * self._args.round_mins
			else:
				this_time = item.abs_value.value

			end_time = current_time + this_time
			begin_time_str = "%d:%02d" % (current_time // 60, current_time % 60)
			end_time_str = "%d:%02d" % (end_time // 60, end_time % 60)
			if this_time >= 60:
				duration_str = "%d:%02d" % (this_time // 60, this_time % 60)
			else:
				duration_str = "%d" % (this_time)
			print("\t\t\t<li><b>%s - %s</b>: %s (%s)</li>" % (begin_time_str, end_time_str, item.text, duration_str))

			current_time = end_time

		print(self._abs_sum, self._rel_sum)

if __name__ == "__main__":
	parser = FriendlyArgumentParser(description = "Agenda parser.")
	parser.add_argument("-b", "--begin-time", metavar = "time", default = "0:00", help = "Begin at this timeslot. Defaults to %(default)s.")
	parser.add_argument("-e", "--end-time", metavar = "time", default = "24:00", help = "End at this timeslot. Defaults to %(default)s.")
	parser.add_argument("-o", "--offset-time", metavar = "time", help = "Offset everything by this amount of time.")
	parser.add_argument("-r", "--round-mins", metavar = "minutes", type = int, default = 5, help = "Round to this many minutes. Defaults to %(default)d minutes.")
	parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increases verbosity. Can be specified multiple times to increase.")
	parser.add_argument("filename", help = "File to parse")
	args = parser.parse_args(sys.argv[1:])

	ap = AgendaParser(args)
	ap.dump()
