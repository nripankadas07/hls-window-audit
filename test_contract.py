import unittest
from hls_window_audit import audit,parse
def fixture(seq=0,disc=0,uris=("a.ts","b.ts"),dur="4"):
    return "#EXTM3U\n#EXT-X-TARGETDURATION:4\n#EXT-X-MEDIA-SEQUENCE:"+str(seq)+"\n#EXT-X-DISCONTINUITY-SEQUENCE:"+str(disc)+"\n"+"".join("#EXTINF:"+dur+",\n"+u+"\n" for u in uris)
class Contract(unittest.TestCase):
    def test_sliding_window(self):
        r=audit(fixture(),fixture(1,uris=("b.ts","c.ts")));self.assertTrue(r["ok"]);self.assertEqual(r["overlap_count"],1)
    def test_changed_uri(self):self.assertFalse(audit(fixture(),fixture(uris=("x.ts","b.ts")))["ok"])
    def test_duration_change(self):self.assertFalse(audit(fixture(),fixture(dur="3"))["ok"])
    def test_discontinuity(self):self.assertFalse(audit(fixture(),fixture(disc=1))["ok"])
    def test_gap(self):self.assertEqual(audit(fixture(),fixture(4))["findings"][0]["missing"],2)
    def test_regression(self):self.assertFalse(audit(fixture(3),fixture(2))["ok"])
    def test_rounding_boundary(self):
        self.assertTrue(audit(fixture(dur="4.49"),fixture(dur="4.49"))["ok"]);self.assertFalse(audit(fixture(dur="4.5"),fixture(dur="4.5"))["ok"])
    def test_bom_crlf(self):self.assertEqual(parse("\ufeff"+fixture().replace("\n","\r\n"))["segments"][0]["sequence"],0)
    def test_duplicate_header(self):
        with self.assertRaises(ValueError):parse(fixture().replace("#EXT-X-TARGETDURATION:4","#EXT-X-TARGETDURATION:4\n#EXT-X-TARGETDURATION:4"))
    def test_unsupported_master(self):
        with self.assertRaises(ValueError):parse("#EXTM3U\n#EXT-X-STREAM-INF:BANDWIDTH=10\na.m3u8")
    def test_missing_uri(self):
        with self.assertRaises(ValueError):parse(fixture()+"#EXTINF:1,\n")
    def test_endlist_mutation(self):self.assertFalse(audit(fixture()+"#EXT-X-ENDLIST\n",fixture())["ok"])
    def test_uri_omitted(self):self.assertNotIn("private.example",str(audit(fixture(uris=("https://private.example/token",)),fixture(uris=("https://private.example/token",)))))
    def test_leading_discontinuity(self):
        text=fixture().replace('#EXTINF:4,','#EXT-X-DISCONTINUITY\n#EXTINF:4,',1)
        self.assertEqual(parse(text)['segments'][0]['discontinuity'],1)
    def test_discontinuity_sequence_order(self):
        text=fixture().replace('#EXT-X-DISCONTINUITY-SEQUENCE:0','#EXT-X-DISCONTINUITY\n#EXT-X-DISCONTINUITY-SEQUENCE:0')
        with self.assertRaises(ValueError):parse(text)
    def test_discontinuity_leaves_sliding_window(self):
        before=fixture().replace('#EXTINF:4,\nb.ts', '#EXT-X-DISCONTINUITY\n#EXTINF:4,\nb.ts')
        after=fixture(1,disc=1,uris=('b.ts','c.ts'))
        self.assertTrue(audit(before,after)['ok'])
