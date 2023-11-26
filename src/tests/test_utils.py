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
