import re
import json

css_code = """
.oa-product-color--zebra-smokey-rose {
    background-color: #c18080;
}

.oa-product-color--zebra-purple {
    background-color: #b5b1e5;
}

.oa-product-color--zebra-power-pink {
    background-color: #dd0585;
}

.oa-product-color--zebra-off-white {
    background-color: #fcf5e3;
}

.oa-product-color--zebra-black {
    background-color: #000000;
}

.oa-product-color--wood-rose {
    background-color: #B57272;
}

.oa-product-color--winter-blush {
    background-color: #f88180;
}

.oa-product-color--wine {
    background-color: #6b2c5f;
}

.oa-product-color--white-rose-purple {
    background-color: #b5b1e5;
}

.oa-product-color--white-multicolor {
    background-color: #ffffff;
}

.oa-product-color--white {
    background-color: #ffffff;
}

.oa-product-color--venice-blue {
    background-color: #789dde;
}

.oa-product-color--velvet-rose {
    background-color: #7e374e;
}

.oa-product-color--velvet-powder {
    background-color: #8e8e8e;
}

.oa-product-color--velvet-plum {
    background-color: #896e8b;
}

.oa-product-color--velvet-black {
    background-color: #000000;
}

.oa-product-color--ultra-violet {
    background-color: #7d6baf;
}

.oa-product-color--turkis {
    background-color: #02b0c8;
}

.oa-product-color--transparent-poppy-orange {
    background-color: #ff8a73;
}

.oa-product-color--toffee-tan {
    background-color: #7a6862;
}

.oa-product-color--taupe-nude {
    background-color: #927f7c;
}

.oa-product-color--taupe-brown {
    background-color: #644139;
}

.oa-product-color--sweet-berry {
    background-color: #cc5c7e;
}

.oa-product-color--sunset-pink {
    background-color: #e96393;
}

.oa-product-color--sunflower-yellow {
    background-color: #f99108;
}

.oa-product-color--sun-yellow {
    background-color: #fff800;
}

.oa-product-color--summer-berry {
    background-color: #d3075a;
}

.oa-product-color--stormy-blue {
    background-color: #465966;
}

.oa-product-color--stone {
    background-color: #d5c7bc;
}

.oa-product-color--steel-grey-tie-dye {
    background-color: #a4a8ab;
}

.oa-product-color--steel-grey {
    background-color: #8e8e8e;
}

.oa-product-color--spearmint {
    background-color: #7d9e89;
}

.oa-product-color--soft-white {
    background-color: #f4eee8;
}

.oa-product-color--soft-sky-blue-tie-dye {
    background-color: #9cc6f7;
}

.oa-product-color--soft-palm-green {
    background-color: #485e5a;
}

.oa-product-color--soft-khaki {
    background-color: #8a9678;
}

.oa-product-color--soft-jade {
    background-color: #8eb2a9;
}

.oa-product-color--soft-camel {
    background-color: #c6ac9b;
}

.oa-product-color--soft-blush {
    background-color: #ce97b4;
}

.oa-product-color--soft-blue {
    background-color: #5a6b72;
}

.oa-product-color--soft-berry {
    background-color: #cc7196;
}

.oa-product-color--smokey-rose-lurex {
    background-color: #c18090;
}

.oa-product-color--smokey-rose {
    background-color: #c18090;
}

.oa-product-color--sky-blue {
    background-color: #66acdd;
}

.oa-product-color--skin {
    background-color: #fad4d4;
}

.oa-product-color--shiny-stone {
    background-color: #d5c7bc;
}

.oa-product-color--shiny-soft-blue {
    background-color: #5a6b72;
}

.oa-product-color--shiny-sand {
    background-color: #ccac92;
}

.oa-product-color--shiny-rose-gold {
    background-color: #e8b1b1;
}

.oa-product-color--shiny-red {
    background-color: #c4060a;
}

.oa-product-color--shiny-pink {
    background-color: #ff50b8;
}

.oa-product-color--shiny-petrol {
    background-color: #00345e;
}

.oa-product-color--shiny-khaki {
    background-color: #404c39;
}

.oa-product-color--shiny-deep-green {
    background-color: #044042;
}

.oa-product-color--shiny-cranberry {
    background-color: #911445;
}

.oa-product-color--shiny-cliff-grey {
    background-color: #514a4e;
}

.oa-product-color--shiny-blue {
    background-color: #37378c;
}

.oa-product-color--shiny-black {
    background-color: #000000;
}

.oa-product-color--shiny-atlantic-blue {
    background-color: #2c3958;
}

.oa-product-color--scarlet-red {
    background-color: #f23041;
}

.oa-product-color--sand {
    background-color: #ccac92;
}

.oa-product-color--rose-white {
    background-color: #ebc8b2;
}

.oa-product-color--rose-red {
    background-color: #d01c1f;
}

.oa-product-color--rose-quartz {
    background-color: #f7cac9;
}

.oa-product-color--rose-melange {
    background-color: #e8b1b1;
}

.oa-product-color--rose-gold {
    background-color: #d99899;
}

.oa-product-color--rose {
    background-color: #e8b1b1;
}

.oa-product-color--rock-crystal {
    background-color: #8e8e8e;
}

.oa-product-color--red {
    background-color: #ff0800;
}

.oa-product-color--purple-melange {
    background-color: #b5b1e5;
}

.oa-product-color--purple {
    background-color: #b5b1e5;
}

.oa-product-color--prism-pink {
    background-color: #ed748b;
}

.oa-product-color--power-pink {
    background-color: #dd0585;
}

.oa-product-color--power-blue {
    background-color: #37378c;
}

.oa-product-color--powder {
    background-color: #8e8e8e;
}

.oa-product-color--poppy-orange-tie-dye {
    background-color: #fc9a8d;
}

.oa-product-color--poppy-orange {
    background-color: #ff8a73;
}

.oa-product-color--petrol {
    background-color: #00345e;
}

.oa-product-color--peach-blush {
    background-color: #ff9fa8;
}

.oa-product-color--pastel-yellow {
    background-color: #f5eabc;
}

.oa-product-color--pastel-green {
    background-color: #d1e7c8;
}

.oa-product-color--paris-pink {
    background-color: #d32e5e;
}

.oa-product-color--papaya-orange {
    background-color: #f9572b;
}

.oa-product-color--palm-green {
    background-color: #2e4c48;
}

.oa-product-color--pale-soft-jade {
    background-color: #e4f6e4;
}

.oa-product-color--pale-rose {
    background-color: #e9c9d1;
}

.oa-product-color--pale-purple {
    background-color: #cec1e0;
}

.oa-product-color--pale-prism-pink {
    background-color: #ff908d;
}

.oa-product-color--pale-poppy-orange-tie-dye {
    background-color: #ff9fa8;
}

.oa-product-color--pale-poppy-orange {
    background-color: #ff9fa8;
}

.oa-product-color--pale-olive {
    background-color: #697c6a;
}

.oa-product-color--pale-jade {
    background-color: #9ab7b0;
}

.oa-product-color--orchid {
    background-color: #c59ec6;
}

.oa-product-color--orange-tie-dye {
    background-color: #ff8a73;
}

.oa-product-color--orange-multi {
    background-color: #ff8a73;
}

.oa-product-color--off-white-zebra {
    background-color: #2e4c48;
}

.oa-product-color--off-white {
    background-color: #faf9f6;
}

.oa-product-color--oceans-blue {
    background-color: #2d2d7a;
}

.oa-product-color--ocean-blue {
    background-color: #6e7e99;
}

.oa-product-color--nude {
    background-color: #ebc8b2;
}

.oa-product-color--none {
    background-color: #ffffff;
}

.oa-product-color--neon-yellow {
    background-color: #f4ff0b;
}

.oa-product-color--neon-pink-tie-dye {
    background-color: #ffb3f6;
}

.oa-product-color--neon-pink {
    background-color: #ff69db;
}

.oa-product-color--navy {
    background-color: #2a3244;
}

.oa-product-color--multicolor {
    background-color: #ffffff;
}

.oa-product-color--multi {
    background-color: #ffffff;
}

.oa-product-color--mint-tie-dye {
    background-color: #b6dfc4;
}

.oa-product-color--macchiato {
    background-color: #aa8977;
}

.oa-product-color--lurex-light-jade {
    background-color: #b6dfc4;
}

.oa-product-color--lurex-light-blue {
    background-color: #a8d8ef;
}

.oa-product-color--lime {
    background-color: #dfef87;
}

.oa-product-color--light-summer-berry {
    background-color: #f185b5;
}

.oa-product-color--light-rose {
    background-color: #ffdbea;
}

.oa-product-color--light-prism-pink {
    background-color: #ffc7c7;
}

.oa-product-color--light-nude {
    background-color: #efe1ca;
}

.oa-product-color--light-jade {
    background-color: #b6dfc4;
}

.oa-product-color--light-island-green {
    background-color: #75c59a;
}

.oa-product-color--light-grey-melange {
    background-color: #e8e8ed;
}

.oa-product-color--light-blue-gardient {
    background-color: #98bcfa;
}

.oa-product-color--light-blue {
    background-color: #a8d8ef;
}

.oa-product-color--leo {
    background-color: #d1a68c;
}

.oa-product-color--khaki {
    background-color: #404c39;
}

.oa-product-color--ivory {
    background-color: #e9d7c7;
}

.oa-product-color--island-green {
    background-color: #008658;
}

.oa-product-color--iced-mint {
    background-color: #a4f0d8;
}

.oa-product-color--grey-melange {
    background-color: #a7a7aa;
}

.oa-product-color--grey {
    background-color: #8e8e8e;
}

.oa-product-color--green-leo-print {
    background-color: #514f3a;
}

.oa-product-color--earth-brown {
    background-color: #927f7c;
}

.oa-product-color--dusty-rose {
    background-color: #c18080;
}

.oa-product-color--dusty-lilac {
    background-color: #98858d;
}

.oa-product-color--dove-blue {
    background-color: #a1bce2;
}

.oa-product-color--deep-green {
    background-color: #044042;
}

.oa-product-color--dazzling-blue {
    background-color: #2e4da7;
}

.oa-product-color--dark-wood-rose {
    background-color: #7d4d55;
}

.oa-product-color--dark-purple {
    background-color: #39075f;
}

.oa-product-color--dark-pink {
    background-color: #921353;
}

.oa-product-color--dark-navy {
    background-color: #2a3244;
}

.oa-product-color--dark-green {
    background-color: #044042;
}

.oa-product-color--dark-dove-blue {
    background-color: #717388;
}

.oa-product-color--dark-camel {
    background-color: #c19a6b;
}

.oa-product-color--dark-anthracite {
    background-color: #3a363a;
}

.oa-product-color--cranberry {
    background-color: #911445;
}

.oa-product-color--coral {
    background-color: #ff7878;
}

.oa-product-color--cool-berry {
    background-color: #84555d;
}

.oa-product-color--cloud-blue {
    background-color: #b1ccdc;
}

.oa-product-color--cliff-grey {
    background-color: #514a4e;
}

.oa-product-color--cherry-chocolate {
    background-color: #602830;
}

.oa-product-color--cha-cha-blush {
    background-color: #f29b9b;
}

.oa-product-color--caramel-brown {
    background-color: #85461e;
}

.oa-product-color--bubblegum {
    background-color: #e46c99;
}

.oa-product-color--brown-leo-print {
    background-color: #644139;
}

.oa-product-color--brown {
    background-color: #8b4f39;
}

.oa-product-color--bright-pink {
    background-color: #dd0585;
}

.oa-product-color--bright-berry {
    background-color: #871659;
}

.oa-product-color--boho-berry {
    background-color: #854c65;
}

.oa-product-color--blush {
    background-color: #a0657d;
}

.oa-product-color--blue {
    background-color: #2d2d7a;
}

.oa-product-color--black-white {
    background-color: #000000;
}

.oa-product-color--black-lurex {
    background-color: #000000;
}

.oa-product-color--black {
    background-color: #000000;
}

.oa-product-color--beige {
    background-color: #e2cfb5;
}

.oa-product-color--beach-dye {
    background-color: #ffcfd3;
}

.oa-product-color--bay-blue {
    background-color: #58c9d4;
}

.oa-product-color--baia-blue {
    background-color: #71b5ab;
}

.oa-product-color--azure-blue {
    background-color: #004c8e;
}

.oa-product-color--aubergine {
    background-color: #4e3c5b;
}

.oa-product-color--atlantic-blue {
    background-color: #2c3958;
}

.oa-product-color--aqua-haze {
    background-color: #82b8bb;
}

.oa-product-color--aqua-gray {
    background-color: #a2b0a8;
}

.oa-product-color--aqua {
    background-color: #56d6ac;
}

.oa-product-color--amethyst {
    background-color: #885e95;
}

.oa-product-color--amber-brown {
    background-color: #9b391f;
}

.oa-product-color--stormy-blue-tie-dye {
    background-color: #465966;
}

.oa-product-color--taupe-nude-tie-dye {
    background-color: #927f7c;
}

.oa-product-color--rose-tie-dye {
    background-color: #e8b1b1;
}

.oa-product-color--multi-pink {
    background-color: #f7afad;
}

.oa-product-color--multi-green {
    background-color: #9ebab9;
}

.oa-product-color--dolphin-blue {
    background-color: #bbcbd3;
}

.oa-product-color--70s-multi {
    background-color: #df1e22;
}

.oa-product-color--plum {
    background-color: #720831;
}

.oa-product-color--smokey-green {
    background-color: #8f9991;
}

.oa-product-color--moss {
    background-color: #343f35;
}

.oa-product-color--rose-water {
    background-color: #ccae9e;
}

.oa-product-color--yellow-stone {
    background-color: #f4e398;
}

.oa-product-color--cool-violet {
    background-color: #6667ab;
}

.oa-product-color--dark-chocolate {
    background-color: #40312f;
}

.oa-product-color--light-beige {
    background-color: #c5bbae;
}

.oa-product-color--sunny-peach {
    background-color: #f4a6a3;
}

.oa-product-color--winter-stone {
    background-color: #c8c1b5;
}

.oa-product-color--light-stone {
    background-color: #e4e1d1;
}

.oa-product-color--cinnamon {
    background-color: #933c1d;
}

.oa-product-color--earth-brown {
    background-color: #927f7c;
}

.oa-product-color--light-orchid {
    background-color: #c6b0d5;
}

.oa-product-color--smaragd-green {
    background-color: #375951;
}

.oa-product-color--frosted-lavender {
    background-color: #bdabbe;
}

.oa-product-color--iris-pink {
    background-color: #c07eb3;
}

.oa-product-color--fire-orange {
    background-color: #f5412a;
}

.oa-product-color--grey-marble {
    background-color: #c6c6c6;
}

.oa-product-color--red-mahagony {
    background-color: #6b4a4d;
}

.oa-product-color--soft-grey {
    background-color: #706f6f;
}

.oa-product-color--wild-berry {
    background-color: #ba6184;
}

.oa-product-color--oatmeal {
    background-color: #c8c0b7;
}

.oa-product-color--fuchsia-pink {
    background-color: #d40064;
}

.oa-product-color--deep-sea-blue {
    background-color: #1e1b49;
}

.oa-product-color--deep-purple {
    background-color: #4c2978;
}

.oa-product-color--cyan {
    background-color: #31b2b6;
}

.oa-product-color--black-multi {
    background-color: #000000;
}

.oa-product-color--soft-cyan-melange {
    background-color: #8dcde8;
}


.oa-product-color--soft-purple-melange {
    background-color: #d6abd2;
}


.oa-product-color--soft-orange-melange {
    background-color: #ee998d;
}


.oa-product-color--oat-milk {
    background-color: #e8e6d9;
}


.oa-product-color--grey-lilac {
    background-color: #696671;
}


.oa-product-color--light-black {
    background-color: #2d2d2d;
}

.oa-product-color--grey-mauve {
    background-color: #655e70;
}

.oa-product-color--oak {
    background-color: #e8e6d9
}

.oa-product-color--diva-pink {
    background-color: #f4a6da;
}

.oa-product-color--hazy-blue {
    background-color: #8ccfea;
}

.oa-product-color--limona,
.oa-product-color--limon {
    background-color: #f6ff9f;
}

.oa-product-color--light-grey-mauve {
    background-color: #9590a0;
}

.oa-product-color--california-rose {
    background-color: #f4dce8;
}

.oa-product-color--hot-pink {
    background-color: #ed7eb3;
}

.oa-product-color--soft-tropical-orange {
    background-color: #f9b795;
}

.oa-product-color--light-hazy-blue {
    background-color: #95d8ef;
}

.oa-product-color--light-hot-pink {
    background-color: #f28fc1;
}

.oa-product-color--light-tropical-orange {
    background-color: #ffd2c0;
}

.oa-product-color--sage-green {
    background-color: #afbfa7;
}

.oa-product-color--ultra-blue {
    background-color: #1c3a77;
}

.oa-product-color--soft-diva-pink {
    background-color: #f2cce9;
}

.oa-product-color--soft-oak {
    background-color: #f9f7ef;
}

.oa-product-color--soft-sage-green {
    background-color: #c1ceba;
}

.oa-product-color--soft-bay-blue {
    background-color: #95b9e5;
}

.oa-product-color--tropical-orange {
    background-color: #fc8359;
}

.oa-product-color--bold-hot-pink {
    background-color: #ed3b90;
}

.oa-product-color--dark-oak {
    background-color: #4e4139;
}

.oa-product-color--blue-moon {
    background-color: #343646;
}

.oa-product-color--deep-magenta {
    background-color: #aa0746;
}

.oa-product-color--marine-blue {
    background-color: #2a3244;
}

.oa-product-color--black-swirl {
    background-color: #27272a;
}

.oa-product-color--deep-plum {
    background-color: #912a46;
}

.oa-product-color--bold-hot-pink-swirl {
    background-color: #ed3b90;
}

.oa-product-color--burnt-orange {
    background-color: #ae472d;
}

.oa-product-color--ice-blue-swirl {
    background-color: #c3e0f4;
}

.oa-product-color--teal {
    background-color: #254963;
}

.oa-product-color--mellow-peach-swirl {
    background-color: #dc7f64;
}

.oa-product-color--snow-white {
    background-color: #e3e3e3;
}

.oa-product-color--forest-green {
    background-color: #46483d
}

.oa-product-color--misty-lavender {
    background-color: #be9cc1
}

.oa-product-color--shadow-lilac {
    background-color: #4c2940
}

.oa-product-color--deep-pine-green {
    background-color: #4a4f3a
}

.oa-product-color--tan {
    background-color: #b4a899
}

.oa-product-color--matcha-green {
    background-color: #c7dd83
}

.oa-product-color--iron-grey {
    background-color: #98979a
}

.oa-product-color--moon-blue {
    background-color: #343646
}

.oa-product-color--glacial-blue {
    background-color: #92b5cb
}

.oa-product-color--crystal-white {
    background-color: #f8faff;
    border: 0.0625rem solid rgba(16, 16, 16, 0.6) !important;
}

.oa-product-color--deep-teal {
    background-color: #243d51
}

.oa-product-color--misty-lavender-swirl {
    background-color: #be9cc1
}

.oa-product-color--glacial-blue-swirl {
    background-color: #92b5cb;
}

.oa-product-color--natural-cream {
    background-color: #dad4c8;
}

.oa-product-color--natural-cream {
    background-color: #dad4c8;
}

.oa-product-color--plain-black {
    background-color: #27272a;
}

.oa-product-color--vivid-green {
    background-color: #009b75;
}

.oa-product-color--autumn-rose {
    background-color: #f5b0bd;
}

.oa-product-color--rose-violet {
    background-color: #c14189;
}

.oa-product-color--candy-red {
    background-color: #b20f2e;
}

.oa-product-color--light-aloe-grey {
    background-color: #8c9fa1;
}

.oa-product-color--light-dawn-blue {
    background-color: #949ac2;
}

.oa-product-color--light-hibiscus-red {
    background-color: #e08087;
}

.oa-product-color--scuffed-lemon {
    background-color: #e3db94;
}

.oa-product-color--dawn-blue {
    background-color: #686b8e;
}

.oa-product-color--hibiscus-red {
    background-color: #db5d69;
}

.oa-product-color--aloe-grey {
    background-color: #5f7278;
}

.oa-product-color--light-scuffed-lemon {
    background-color: #f4ecc2;
}

.oa-product-color-- * {
    border: 0.0625rem solid rgba(16, 16, 16, 0.3);
}
"""


def remove_span_tags(html_text):
    """Removes HTML span tags from a string.

    The opening and closing tags are removed separately to avoid overlapping
    tags. The text between the tags is preserved. The span tags can also
    have various attributes in the opening tag.

    Args:
        html_text: The HTML text to remove the <span> tags from.

    Returns:
        The HTML text with the <span> tags removed, but inner text
        preserved.
    """
    # Capture <span> tags, open and close separately to avoid overlapping
    # <span\s*.*?> because there can be attributes in the opening tag
    s = re.compile(r"<span\s*.*?>")
    s2 = re.compile(r"</span>")

    # Replace <span> tags with their inner text in the value
    text = re.sub(s, "", html_text)
    cleaned_text = re.sub(s2, "", text)
    return cleaned_text


if __name__ == "__main__":
    # print(["leggings", "underwear"].split(","))
    # data = ["Brown", "colors_digital-seamless-leggings", "Taupe_color"]
    # print(
    #     next(
    #         (item.split("_")[0].lower() for item in data if "_color" in item),
    #         None,
    #     )
    # )

    # t = (
    #     "<b>Fabric Content: </b>Leotard: 82% Polyester / 18% Spandex | "
    #     "Straps: 80% Nylon / 20% Spandex<br><br>"
    # )
    #
    # pattern = re.compile(
    #     r"(?P<percentage>\d{1,3}(?:\.\d{1,2})?(?:\s*|&nbsp;)%)(?:\s*|&nbsp;)"
    #     r"(?P<material>[\w\s]+?)(?=\s*,|\s*<|\s*(?:\d{1,3}\s?%|$|\s*[&.]|"
    #     r"\s*und|\s*\/|\s*\|))"
    # )
    #
    # matches = pattern.findall(t)
    # print(matches)
    # # Concatenate percentage and material, convert material to lowercase
    # result = [
    #     f"{percentage.replace(' ', '').strip()} {material.lower()}"
    #     for percentage, material in matches
    # ]
    #
    # print(result)

    # Extract color names and codes using regular expression
    color_pattern = r"\.oa-product-color--([^{\s,]+)(?:\s*,\s*\.oa-product-color--([^{\s,]+))?(?:[^#]*#([a-fA-F0-9]+);[^}]*)?"
    matches = re.findall(color_pattern, css_code)

    # Create a dictionary from the extracted data
    color_dict = {}
    for name1, name2, code in matches:
        if name1 and code:
            color_dict[name1.strip()] = f"#{code}"
        if name2 and code:
            color_dict[name2.strip()] = f"#{code}"

    # Convert the dictionary to a JSON object
    json_result = json.dumps(color_dict, indent=4)

    # Print or use the JSON object as needed
    print(json_result)
