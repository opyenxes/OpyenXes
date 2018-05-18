from opyenxes.out.XMxmlSerializer import XMxmlSerializer
import gzip


class XMxmlGZIPSerializer(XMxmlSerializer):
    """Compressed MXML serialization for XES data (legacy implementation).
    Note that this serialization may be lossy, you should preferrably use the
    XES.XML serialization for XES data.

    """
    def serialize(self, log, out, in_bytes=False):
        """Serializes a given log to the given output stream.

        :param log: Log to be serialized.
        :type log: `XLog`
        :param out:  TextIOWrapper for serialization.
        :type out: _io.TextIOWrapper
        :param in_bytes: Private argument to decide if serialized as bytes or as string
        :type in_bytes: bool
        """
        path = out.name
        out.close()
        with gzip.open(path, "wb") as file:
            super().serialize(log, file, True)

    @staticmethod
    def get_suffices():
        """Returns an array of possible file suffices for this serialization.

        :return: An array of possible file suffices for this serialization.
        :rtype: list[str]
        """
        return ["mxml.gz"]
