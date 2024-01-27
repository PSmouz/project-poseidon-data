"""
Test the utils module.
"""

import unittest

from src.utils import extract_materials, parse_css_colors


class ExtractMaterialsTest(unittest.TestCase):
    def test_extract_materials_single_material(self):
        value = "Material: 100% Cotton"
        expected_result = ["100% cotton"]
        result = extract_materials(value)
        self.assertEqual(result, expected_result)

    def test_extract_materials_multiple_materials(self):
        value = "Material: 54 % Polyamide, 39 % Polyester & 7 % Elasthan."
        expected_result = ["54% polyamide", "39% polyester", "7% elasthan"]
        result = extract_materials(value)
        self.assertEqual(result, expected_result)

    def test_extract_materials_german_und_keyword(self):
        value = "Material: 65 % Cotton und 35 % Polyester"
        expected_result = ["65% cotton", "35% polyester"]
        result = extract_materials(value)
        self.assertEqual(result, expected_result)

    def test_teveo_case_1(self):
        """Teveo Case 1: 65 % Cotton und 35 % Polyester"""
        value = """<h3>Produktdetails</h3><p>Create your <strong>Signature
        </strong> TEVEO Look! Unsere <strong>Signature Scrunch Leggings in
        Graphit </strong> <span> betont deinen Kurven und gibt dir einen
        optimalen Fit für dein Training. Durch den Booty Scrunch sowie der
        Booty-Kontur mit Kompression wird dein Gesäß optisch angehoben und
        formt einen schönen runden Po. </span></p><p>Die Leggings ist in vier
        weiteren Farben erhältlich und perfekt mit unserem Signature Neckholder
        Bh, Signature Twisted Bh oder Signature Oversized Sweater kombinierbar.
        </p><ul><li>Qualitativ hochwertiges Logo</li><li>Superweiches angenehmes
         Material<br></li><li>Booty Scrunch &amp; Booty Kontur</li></ul><h3>
         Passform</h3><p>Camilla ist <span data-mce-fragment="1">1,72</span>
         m und trägt Größe XS.</p><h3>Material &amp; Pflege</h3><p>Material:
         65 % Cotton und 35 % Polyester. Bitte nur bei 30 Grad mit ähnlichen
         Farben waschen und nicht in den Trockner geben.</p>"""
        expected_result = ["65% cotton", "35% polyester"]
        result = extract_materials(value)
        self.assertEqual(result, expected_result)

    def test_teveo_case_2(self):
        """Teveo Case 2: 54 % Polyamide, 39 % Polyester & 7 % Elasthan."""
        value = """<h3>Produktdetails</h3><p>Mit deiner <strong>Tie Dye
        Scrunch Leggings in Cold</strong> stichst du garantiert aus der
        Masse heraus! Und das Beste daran ist, dass du damit ein Unikat
        besitzt. Denn jede Tie Dye Scrunch Leggings wird individuell gefärbt
         und ergibt dadurch eine <strong>einzigartige Färbung</strong>.</p>
         <p>Gleichzeitig sticht sie nicht nur durch ihre auffälligen Farben
         ins Auge, sondern auch, weil sie deine Kruven gekonnt in Szene
         setzt. So formt die Leggings mit dem <strong>Booty-Scrunch</strong>
          einen tollen Po und kaschiert durch den High-Waist-Fit deine
          Taille vorteilhaft.</p><p>Die Tie Dye Scrunch Leggings in Cold
          lässt sich toll mit unseren Everyday Tops und Sport Bhs
          kombinieren. <span>Hier findest du noch einmal alle Vorteile der
          Tie Dye Scrunch Leggings Cold auf einen Blick:</span></p><ul><li>
          Booty Scrunch</li><li>Einzigartiges Design</li><li>Superweiches
          angenehmes Material</li><li>Qualitatives gestricktes Logo</li>
          </ul><br><h3>Größe &amp; Passform</h3><p>Hannah ist 1,62 m und
          trägt Größe S (fällt größengerecht aus, wenn du zwischen zwei
          Größen schwankst, empfehlen wir die größere zu nehmen).</p><br>
          <h3>Material &amp; Pflege</h3><p>Material: 54 % Polyamide, 39 %
          Polyester &amp; 7% Elasthan. Bitte nur bei 30 Grad mit ähnlichen
          Farben waschen und nicht in den Trockner geben. Am Besten in einem
           Wäschenetz waschen.</p>"""
        expected_result = ["54% polyamide", "39% polyester", "7% elasthan"]
        result = extract_materials(value)
        self.assertEqual(result, expected_result)

    def test_teveo_case_3(self):
        """Teveo Case 3: 90% Polyamid & 10% Elasthan."""
        value = """<h3>Produktdetails</h3><br><p>Wir präsentieren stolz unsere
        erste recycelte Kollektion: die Ribbed Kollektion! Hergestellt aus einem
         flexiblen, gerippten und recycelten Garn, ist diese Kollektion ein
         absolutes Must-Have. Ein besonderer Hingucker ist dabei die Schnürung,
         welche deinem Outfit eine elegante Note verleiht. Somit ist unsere
         Leggings perfekt für dein Training, deinen Rest-Day oder deinen Alltag
         geeignet. Du wirst sie lieben!</p><br><p>Am Besten kombinierst du
         unsere Ribbed Leggings mit unseren Ribbed Crop Tops oder Ribbed BHs.
         </p><br><ul><li>Recycelter Garn</li><li>Ribbed seamless Design</li><li>
         Edles, gestricktes Logo</li></ul><br><h3>Größe &amp; Passform</h3><br>
         <p>Kim ist 1,72 m &amp; trägt Größe M.</p><br><h3>Material &amp; Pflege
         </h3><br><p>Recycelter Garn: 90% Polyamid &amp; 10% Elasthan.Bitte nur
         bei 30 Grad mit ähnlichen Farben waschen und nicht in den Trockner
         geben.</p>"""
        expected_result = ["90% polyamid", "10% elasthan"]
        result = extract_materials(value)
        self.assertEqual(result, expected_result)

    def test_oa_case_1(self):
        """Oceansapart Case 1:"""
        value = """<ul><li>Leggings with Belt Detail</li><li>Support level: 
        Medium</li><li>Reflective Silicone transfer print</li><li>Shell fabric 
        round cord fixed at sides for beltloops</li><li>Wide waistband</li><li>
        Silicone tape inside top of waistband to prevent slipping</li><li>
        Heartshaped waistband stitching on back of pant that shape the butt</li>
        <li>Shape level: Medium</li><li>Fit: Tight</li><li>Rise height: High 
        rise</li><li>Leggings fit</li><li>Plain Knit</li><li>Breathable</li><li>
        Soft touch</li><li>Sweat wicking</li><li>Second skin feeling</li><li>
        Four-way stretch</li><li>OASoftSense is a fabric that is engineered for 
        a soft, comfortable, and sensory promotes a feeling of well-being and 
        relaxation for the wearer.</li><li>80% Polyamide 20% Elastane</li></ul>
        """
        expected_result = ["80% polyamide", "20% elastane"]
        result = extract_materials(value)
        self.assertEqual(result, expected_result)

    def test_oa_case_2(self):
        """Oceansapart Case 2:"""
        value = """<ul><li>High Waist</li><li>Seamless technology</li><li>
        94% recycled polyamide &amp; 6% elastane</li></ul>"""
        expected_result = ["94% recycled polyamide", "6% elastane"]
        result = extract_materials(value)
        self.assertEqual(result, expected_result)

    def test_oa_case_3(self):
        """Oceansapart Case 3:"""
        value = """<ul><li>Warming Straight Leg Pant</li><li>Tonal logo print
        </li><li>Two seam pockets with zippers</li><li>Lock zippers</li><li>High
         rise</li><li>Body flattering seams on the sides of the leg</li><li>
         Shaping waistband</li><li>Heart shape on back that empasized shape of 
         the butt</li><li>Super warming</li><li>Warming material</li><li>Brushed
          inside</li><li>Soft on skin feeling</li><li>UV protective</li><li>
          Slight stretch</li><li>80% Poliestere, 20% Elastan</li></ul>"""
        expected_result = ["80% poliestere", "20% elastan"]
        result = extract_materials(value)
        self.assertEqual(result, expected_result)

    def test_nvgtn_case_1(self):
        """NVGTN Case 1:"""
        value = """<meta charset="utf-8"><meta charset="utf-8"><p><span 
        style="font-weight: 400;">Crush goals and hearts in the sleek and 
        powerful Performance Seamless Leggings. Crafted from the same buttery 
        soft blend of materials that make up our Contour 2.0 Leggings, these 
        leggings have unmatched comfort while keeping up with your every move. 
        The </span><span style="font-weight: 400;">compressive waistband hugs 
        your waist, while the dramatic contour shading accentuates your glutes 
        and legs leaving you looking sculpted, while feeling supported.</span>
        </p><br><p><span style="font-weight: 400;">- Nylon, polyester and 
        spandex</span></p><p><span style="font-weight: 400;">- Fabric feels… 
        lightweight, soft, stretchy</span></p><p><span style="font-weight: 
        400;">- High waisted </span></p><p><span style="font-weight: 400;">- 
        Compressive waistband</span></p><p><span style="font-weight: 400;">- 
        Leg and glute contour shading</span></p><p><span style="font-weight: 
        400;">- Seamless</span><br></p><h5>Model Specs</h5><meta 
        charset="utf-8"><p><span style="font-weight: 400;">Height: 5'2"</span>
        </p><p><span style="font-weight: 400;">Bust: 32"</span></p><p><span 
        style="font-weight: 400;">Waist: 24”</span></p><p><span 
        style="font-weight: 400;">Hips: 36”</span></p><p><span style="font-
        weight: 400;">Size: XS</span></p><h5><span mce-data-marked="1">Material 
        Make-Up</span></h5><p><span style="font-weight: 400;">54% Nylon</span>
        </p><p><span style="font-weight: 400;">30% Polyester</span></p><p><span 
        style="font-weight: 400;">16% Spandex</span><br></p><div 
        style="position: absolute; left: -22px; top: 378.594px;" id="gtx-trans">
        <div class="gtx-trans-icon"><br></div></div>"""
        expected_result = ["54% nylon", "30% polyester", "16% spandex"]
        result = extract_materials(value)
        self.assertEqual(result, expected_result)

    def test_nvgtn_case_2(self):
        """NVGTN Case 2:"""
        value = """<meta charset="utf-8"><meta charset="utf-8"><p><span>Turn 
        heads and strut with confidence in the gym with our new NVGTN Contour 
        seamless leggings. These leggings have contour shadowing designed to 
        enhance the beauty of your natural curves. Made with a buttery soft 
        blend of materials, these leggings will feel weightless on your body 
        while hugging you in all the right places, allowing you to crush your 
        workout without any disturbances or discomforts. These leggings are a 
        must have in your gym wardrobe and pair perfectly with our seamless crop
         tops!</span></p><br><p>- Nylon and spandex</p><p>- Fabric feels… 
         lightweight, soft, stretchy</p><p>- High waisted </p><p>- 
         Compressive waistband</p><p>- Thigh and glute contour shading</p><p>- 
         Seamless</p><ul></ul><h5>Model Specs</h5><meta charset="utf-8"><p><span
          style="font-weight: 400;">Height: 5'2"</span></p><p><span style="font-
          weight: 400;">Bust: 32"</span></p><p><span style="font-weight: 400;">
          Waist: 24”</span></p><p><span style="font-weight: 400;">Hips: 36”
          </span></p><p><span style="font-weight: 400;">Size: XS</span></p><h5>
          <span>Material Make-Up</span></h5><p><meta charset="utf-8">
          <span>87% </span><span>Nylon</span><br><span>13</span><span>% 
          </span><span>Spandex</span></p><div style="position: absolute; left: 
          -4px; top: 378.594px;" id="gtx-trans"><div class="gtx-trans-icon">
          </div></div>"""
        expected_result = ["87% nylon", "13% spandex"]
        result = extract_materials(value)
        self.assertEqual(result, expected_result)

    def test_alphalete_case_1(self):
        """Alphalete Case 1:"""
        value = """\u003cmeta charset=\"utf-8\"\u003e\n\u003cp 
        data-mce-fragment=\"1\"\u003e\u003cb 
        data-mce-fragment=\"1\"\u003e\u003ci 
        data-mce-fragment=\"1\"\u003eHIGHLIGHTS\u003c\/i\u003e\u003c\/b\u003e
        \u003c\/p\u003e\n\u003cul data-mce-fragment=\"1\"\u003e\n\u003cli 
        class=\"li1\" data-mce-fragment=\"1\"\u003e\n\u003cspan class=\"s1\" 
        data-mce-fragment=\"1\"\u003e\u003c\/span\u003eSculpting 
        seamlines\u003c\/li\u003e\n\u003cli class=\"li1\" 
        data-mce-fragment=\"1\"\u003eButtery soft hand 
        feel\u003c\/li\u003e\n\u003cli class=\"li1\" 
        data-mce-fragment=\"1\"\u003eHigh Stretch\u003c\/li\u003e\n\u003cli 
        class=\"li1\" data-mce-fragment=\"1\"\u003eFlared 
        leg\u003c\/li\u003e\n\u003c\/ul\u003e\n\u003cp 
        data-mce-fragment=\"1\"\u003e\u003cb 
        data-mce-fragment=\"1\"\u003e\u003ci data-mce-fragment=\"1\"\u003eFIT 
        SUGGESTION\u003c\/i\u003e\u003c\/b\u003e\u003c\/p\u003e\n\u003cul 
        data-mce-fragment=\"1\"\u003e\n\u003cli 
        data-mce-fragment=\"1\"\u003e\n\u003cspan 
        data-mce-fragment=\"1\"\u003e\u003c\/span\u003eThis item&nbsp;runs 
        true to Alphalete's standard sizing.\u003c\/li\u003e\n\u003cli 
        data-mce-fragment=\"1\"\u003e\n\u003cspan 
        data-mce-fragment=\"1\"\u003e\u003c\/span\u003eWe recommend sizing up 
        for a more relaxed fit or down for a more compressive 
        fit.\u003c\/li\u003e\n\u003cli 
        data-mce-fragment=\"1\"\u003e\n\u003cspan 
        data-mce-fragment=\"1\"\u003e\u003c\/span\u003eModel is 
        5’10”\/177.8cm, wearing a size\u003cspan 
        data-mce-fragment=\"1\"\u003e&nbsp;M\u003c\/span\u003e\u003cspan 
        data-mce-fragment=\"1\"\u003e&nbsp;\u003c\/span\u003ewith 
        40\"\/101.6cm hips and 28”\/71.1cm 
        waist.\u003c\/li\u003e\n\u003c\/ul\u003e\n\u003cp 
        data-mce-fragment=\"1\"\u003e\u003cb 
        data-mce-fragment=\"1\"\u003e\u003ci 
        data-mce-fragment=\"1\"\u003eMATERIALS AND WASHING 
        DIRECTIONS\u003c\/i\u003e\u003c\/b\u003e\u003c\/p\u003e\n\u003cul 
        data-mce-fragment=\"1\"\u003e\n\u003cli 
        data-mce-fragment=\"1\"\u003e\n\u003cspan 
        data-mce-fragment=\"1\"\u003e\u003c\/span\u003e75%\u003cspan 
        data-mce-fragment=\"1\"\u003e&nbsp;\u003c\/span\u003eNylon,\u003cspan 
        data-mce-fragment=\"1\"\u003e&nbsp;\u003c\/span\u003e25%\u003cspan 
        data-mce-fragment=\"1\"\u003e&nbsp;\u003c\/span\u003eSpandex\u003c
        \/li\u003e\n\u003cli data-mce-fragment=\"1\"\u003e\n\u003cspan 
        data-mce-fragment=\"1\"\u003e\u003c\/span\u003eWe recommend washing 
        inside-out on a cold setting\u003c\/li\u003e\n\u003cli 
        data-mce-fragment=\"1\"\u003e\n\u003cspan 
        data-mce-fragment=\"1\"\u003e\u003c\/span\u003eHang to 
        dry\u003c\/li\u003e\n\u003c\/ul\u003e\n\u003cp 
        data-mce-fragment=\"1\"\u003e\u003cb 
        data-mce-fragment=\"1\"\u003e\u003ci 
        data-mce-fragment=\"1\"\u003eDESCRIPTION\u003c\/i\u003e\u003c\/b
        \u003e\u003c\/p\u003e\n\u003cp data-mce-fragment=\"1\"\u003eDiscover 
        a fusion of supreme comfort and high-stretch compression with our new 
        Aura fabric. Made with irresistibly soft, brushed fabric, 
        our&nbsp;pants\u003cspan 
        data-mce-fragment=\"1\"\u003e&nbsp;\u003c\/span\u003eoffer you 
        unrestricted movement whether you're headed to the gym, a yoga class, 
        or simply lounging at home. We've strategically placed sculpting 
        seamlines to not only draw in the waist but also enhance the natural 
        shape of the glutes.&nbsp;\u003c\/p\u003e"""

        expected_result = ["75% nylon", "25% spandex"]
        result = extract_materials(value)
        self.assertEqual(result, expected_result)

    def test_alphalete_case_2(self):
        """Alphalete Case 2:"""
        value = """<meta charset="UTF-8"><p data-mce-fragment="1"><b 
        data-mce-fragment="1"><i data-mce-fragment="1">HIGHLIGHTS</i></b></p>
        <ul data-mce-fragment="1"><li><span></span>Moisture wicking</li><li>
        <span></span>Medium impact performance<span class="Apple-converted-
        space">&nbsp;</span></li><li><span></span>Super high waisted style fit
        </li><li><span></span>No front rise</li><li><span></span>25” inseam</li>
        <li><span></span>Reinforced stitching<span class="Apple-converted-space"
        >&nbsp;</span></li><li><span></span>Alphalete script logo in silicone
        </li></ul><p data-mce-fragment="1"><br data-mce-fragment="1"></p><p 
        data-mce-fragment="1"><b data-mce-fragment="1"><i data-mce-fragment="1">
        FIT SUGGESTION</i></b></p><ul data-mce-fragment="1"><li data-mce-
        fragment="1"><span data-mce-fragment="1"></span><span data-mce-fragment
        ="1">This item runs true to Alphalete’s standard fit</span>.</li>
        <li class="li2" data-mce-fragment="1">If you are between sizes, we 
        recommend sizing up.</li><li data-mce-fragment="1"><span data-mce-
        fragment="1"></span><span data-mce-fragment="1">Model is <meta charset=
        "UTF-8">5’5”/165cm, wearing a size S with a 27”/68cm waist and 
        38”/96.5cm hips.</span></li></ul><p data-mce-fragment="1"><br data-mce-
        fragment="1"></p><p data-mce-fragment="1"><b data-mce-fragment="1"><i 
        data-mce-fragment="1">MATERIALS AND WASHING DIRECTIONS</i></b></p><ul 
        data-mce-fragment="1"><li data-mce-fragment="1"><span data-mce-
        fragment="1"></span>78% Nylon, 22%&nbsp;Elastane</li><li data-mce-
        fragment="1"><span data-mce-fragment="1"></span>We recommend washing 
        inside-out on a cold setting</li><li data-mce-fragment="1"><span data-
        mce-fragment="1"></span>Hang to dry</li></ul><p data-mce-fragment="1">
        <br data-mce-fragment="1"></p><p data-mce-fragment="1"><b data-mce-
        fragment="1"><i data-mce-fragment="1">DESCRIPTION</i></b></p><p>The 
        Pulse Collection is made with our signature Nylon / Elastane blend; 
        a high-performance material that offers incredible breathability and the
         right amount of compression. The fabric is slick and soft, yet 
         extremely performant and supportive. At its core, Pulse is the electric
          current that brings the much needed spark back into your day and with
           its ability to evaporate moisture quickly, it will always keep you 
           looking and feeling your best.</p>"""

        expected_result = ["78% nylon", "22% elastane"]
        result = extract_materials(value)
        self.assertEqual(result, expected_result)

    def test_alphalete_case_3(self):
        """Alphalete Case 3:"""
        value = """<meta charset="utf-8"><h4 class="p1" data-mce-fragment="1">
        <b data-mce-fragment="1"><i data-mce-fragment="1">HIGHLIGHTS</i></b>
        </h4><ul class="ul1" data-mce-fragment="1"><li class="li1"><span class=
        "s1"></span>Stretchy cotton material</li><li class="li1"><span class=
        "s1"></span>Low impact</li><li class="li1"><span class="s1"></span>
        Rounded camisole neckline</li><li class="li1"><span class="s1"></span>
        Easily adjustable straps</li><li class="li1"><span class="s1"></span>
        Reinforced binding arm and neckline finishing</li><li class="li1"><span 
        class="s1"></span>Custom jacquard waistband with knitted in Alphalete 
        wordmark</li><li class="li1"><span class="s1"></span>Double layered bra 
        construction</li></ul><h4 class="p1" data-mce-fragment="1"><b data-mce-
        fragment="1"><i data-mce-fragment="1">FIT SUGGESTION</i></b></h4><ul 
        class="ul1" data-mce-fragment="1"><li class="li2" data-mce-fragment="1">
        <span class="s1" data-mce-fragment="1"></span>This item runs true to 
        Alphalete’s standard fit.</li><li class="li2" data-mce-fragment="1">
        <span class="s1" data-mce-fragment="1"></span>If you are between sizes, 
        we recommend sizing up for a relaxed fit.</li><li class="li2" data-mce-
        fragment="1"><span class="s1" data-mce-fragment="1"></span>Model is 
        5’8”/1172cm, wearing a size XS with a 31”/78.7cm bust.</li></ul><h4 
        class="p1" data-mce-fragment="1"><b data-mce-fragment="1"><i data-mce-
        fragment="1">MATERIALS AND WASHING DIRECTIONS</i></b></h4><ul class=
        "ul1" data-mce-fragment="1"><li class="li1"><span class="s1"></span>
        46.5% Cotton, 46.5% Modal, 7% Elastane</li><li class="li1">We recommend 
        washing inside-out on a cold setting<span class="s1"></span></li><li 
        class="li1">Hang to dry</li></ul><p class="p1">Introducing our new 
        intimates collection, crafted from soft, comfortable cotton for a loungy
         feel. Our Acute collection features a variety of intimate pieces in 
         different styles and sizes that are perfect for everyday wear or 
         special occasions. Made from a blend of cotton for breathability, modal
          for a soft elevated smooth feel and elastane for improved comfort and 
          shape retention. Our intimates are made to make you feel confident and
           comfortable throughout the day.</p>"""

        expected_result = ["46.5% cotton", "46.5% modal", "7% elastane"]
        result = extract_materials(value)
        self.assertEqual(result, expected_result)

    def test_gkelite_case_1(self):
        """GKElite Case 1:"""
        value = """In the world of gymnastics, confidence is key. The Results 
        Tank Leotard embodies the self-assured spirit of Jade Carey, who feels 
        most confident when she puts in the hard work. The sublimated blue and 
        white pattern on the navy tank leotard represent dedication and 
        tenacity, and the Silver Matte Spanglez™ on the front chest capture the
         shimmer of victory. In this tank leotard designed by Jade herself, you 
         can conquer the mat with confidence knowing that you’re ready to be 
         there!<br><br><b>Features &amp; Benefits</b><ul><li>Jade Carey 
         gymnastics leotard</li>	<li>GK x Jade logo on left hip</li>	<li>
         Workout / Traditional leg cut</li>	<li>Workout tank sleeve</li><li>Navy
          tank leotard</li>	<li>Sublimated blue and white pattern</li>	<li>
          Silver Matte Spanglez™ on front chest</li>	<li>Matching royal 
          scrunchie</li>	<li>Scoop neck front</li>	<li>Straight strap back
          </li>	<li>Leotard designed by Jade Carey</li></ul><br><b>Fabric 
          Content: </b>Leotard: 82% Polyester / 18% Spandex | Straps: 80% Nylon 
          / 20% Spandex<br><br>The scoop neck front and straight strap back 
          provide both style and functionality, ensuring you're ready for every 
          routine, while The GK x Jade logo on the left hip represents a 
          partnership that celebrates excellence. When those competition-day 
          nerves kick in, remember Jade's advice, “take a deep breath and trust 
          in your training.” With a matching rich royal scrunchie to complete 
          the look, you'll be geared up to get results!<br><br>Jade is a star 
          among stars, and you can shine at every practice in these <a href="
          https://www.gkelite.com/collections/jade-carey">leotards</a> designed 
          by Jade herself!<br><br>Placing an order for your team or pro shop? 
          <a href="https://www.gkelite.com/account/login">Log in</a> to see 
          dealer pricing or contact your local <a href="https://www.gkelite.com/
          pages/gk-gym-us-sales-team">GK Sales Representative</a> today."""

        expected_result = ["82% polyester", "18% spandex"]
        result = extract_materials(value)
        self.assertEqual(result, expected_result)


class ParseCSSColorsTest(unittest.TestCase):
    def test_case_1(self):
        value = parse_css_colors(
            ".oa-product-color--limona,.oa-product-color--limon {"
            "background-color: #f6ff9f;}"
        )
        expected_result = {
            "oa-product-color--limona": "#f6ff9f",
            "oa-product-color--limon": "#f6ff9f",
        }
        result = extract_materials(value)
        self.assertEqual(result, expected_result)

    def test_case_2(self):
        value = parse_css_colors(
            ".oa-product-color--moon-blue {background-color: #343646}"
        )
        expected_result = {
            "oa-product-color--moon-blue": "#343646",
        }
        result = extract_materials(value)
        self.assertEqual(result, expected_result)

    def test_case_3(self):
        value = parse_css_colors(
            ".oa-product-color--crystal-white {background-color: "
            "#f8faff;border: 0.0625rem solid rgba(16, 16, 16, 0.6) !important;}"
        )
        expected_result = {
            "oa-product-color--crystal-white": "#f8faff",
        }
        result = extract_materials(value)
        self.assertEqual(result, expected_result)

    def test_case_4(self):
        value = parse_css_colors(
            ".oa-product-color--bold-hot-pink-swirl {background-color: "
            "#ed3b90;}"
        )
        expected_result = {
            "oa-product-color--bold-hot-pink-swirl": "#ed3b90",
        }
        result = extract_materials(value)
        self.assertEqual(result, expected_result)

    def test_case_5(self):
        value = parse_css_colors(
            ".oa-product-color-- * {border: 0.0625rem solid rgba(16, 16, 16, "
            "0.3);}"
        )
        expected_result = {}
        result = extract_materials(value)
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()


#  NVTGN TEST


# Not handled yet
