
INSERT INTO "public"."menu_item" ("id", "name_uni", "name_zawgyi", "unit_price", "description_uni", "description_zawgyi", "menu_category_id", "menu_id") VALUES ('1', 'ပဲသုတ်', 'ပဲသုတ်', '500', 'နှစ်ယောက်စာ ပဲသုတ် ဖြစ်ပါတယ်', '', '1', '1');
INSERT INTO "public"."menu_item" ("id", "name_uni", "name_zawgyi", "unit_price", "description_uni", "description_zawgyi", "menu_category_id",  "menu_id") VALUES ('2', 'အာလူးစမူဆာ ', 'အာလူးစမူဆာ ', '100', 'အာလူးစမူဆာ ', '', '1',  '1');
INSERT INTO "public"."menu_item" ("id", "name_uni", "name_zawgyi", "unit_price", "description_uni", "description_zawgyi", "menu_category_id",  "menu_id") VALUES ('3', 'ကီးမား စမူဆာ', 'ကီးမား စမူဆာ', '200', 'ကီးမား စမူဆာ', '', '1',  '1');
INSERT INTO "public"."menu_item" ("id", "name_uni", "name_zawgyi", "unit_price", "description_uni", "description_zawgyi", "menu_category_id",  "menu_id") VALUES ('4', 'ဗယာကြော်', 'ဗယာကြော်', '100', 'ကဗယာကြော်', '', '1', '1');
INSERT INTO "public"."menu_item" ("id", "name_uni", "name_zawgyi", "unit_price", "description_uni", "description_zawgyi", "menu_category_id", "menu_id") VALUES ('5', 'မပဲကြော်', 'မပဲကြော်', '100', 'မပဲကြော်', '', '1',  '1');
INSERT INTO "public"."menu_item" ("id", "name_uni", "name_zawgyi", "unit_price", "description_uni", "description_zawgyi", "menu_category_id",  "menu_id") VALUES ('6', 'ကြာဇံကြော်', 'ကြာဇံကြော်', '500', 'ကြာဇံကြော်', '', '1',  '1');
INSERT INTO "public"."menu_item" ("id", "name_uni", "name_zawgyi", "unit_price", "description_uni", "description_zawgyi", "menu_category_id", "menu_id") VALUES ('7', 'ခေါက်ဆွဲကြော်', 'ခေါက်ဆွဲကြော်', '500', 'ခေါက်ဆွဲကြော်', '', '1', '2');
INSERT INTO "public"."menu_item" ("id", "name_uni", "name_zawgyi", "unit_price", "description_uni", "description_zawgyi", "menu_category_id", "menu_id") VALUES ('8', 'ဖာလူဒါ', 'ဖာလူဒါ', '1000', 'ဖာလူဒါ', '', '3',  '3');


INSERT INTO "public"."menu_category" ("id", "name_uni", "name_zawgyi") VALUES ('1', 'အကြော်', 'အကြော်');
INSERT INTO "public"."menu_category" ("id", "name_uni", "name_zawgyi") VALUES ('2', 'အချိူပွဲ', 'အချိူပွဲ');
INSERT INTO "public"."menu_category" ("id", "name_uni", "name_zawgyi") VALUES ('3', 'စွပ်ပြုတ်', 'စွပ်ပြုတ်');




INSERT INTO "public"."menu" ("id", "name_uni", "name_zawgyi" ) VALUES ('1', 'ကာဆင်ဘိုင် ပဲသုတ် နှင့်အကြော်', 'ကာဆင်ဘိုင်' );
INSERT INTO "public"."menu" ("id", "name_uni", "name_zawgyi" ) VALUES ('2', 'ယာဆင်ဘိုင်', 'ယာဆင်ဘိုင် ခေါက်ဆွဲကြော်');
INSERT INTO "public"."menu" ("id", "name_uni", "name_zawgyi") VALUES ('3', 'ခါမွရ်ကီး', 'ခါမွရ်ကီး');


INSERT INTO "public"."shop" ("id", "name_uni", "name_zawgyi","description", "lat", "lon", "menu_id","phone_number_1","phone_number_2","phone_number_3", "address", "township_id", "region_id") VALUES ('1', 'ရောင်နက်ဗလီ ရှေ့ ကဆင်ဘိုင်', 'ရောင်နက်ဗလီ ရှေ့ ကဆင်ဘိုင်','ရမ်ဇမ် လအတွက်သာဖွင့်သောဆိုင်ဖြစ်ပါသည်', '16.7894243', '96.1672589', '0','+11111','+11111','+11111', '', '0', '0');
INSERT INTO "public"."shop" ("id", "name_uni", "name_zawgyi","description", "lat", "lon", "menu_id","phone_number_1","phone_number_2","phone_number_3", "address", "township_id", "region_id") VALUES ('2', 'ရောင်နက်ဗလီ ရှေ့ ကဆင်ဘိုင်', 'ရောင်နက်ဗလီ ရှေ့ ဇမ်ဇမ်','ရမ်ဇမ် လအတွက်သာဖွင့်သောဆိုင်ဖြစ်ပါသည်', '16.7895347', '96.1684766', '0','+11111','+11111','+11111', '', '0', '0');
INSERT INTO "public"."shop" ("id", "name_uni", "name_zawgyi","description", "lat", "lon", "menu_id","phone_number_1","phone_number_2","phone_number_3", "address", "township_id", "region_id") VALUES ('3', 'ရောင်နက်ဗလီ ရှေ့ ဟူစိန်ဘိုင် ဖရဲသီး', 'ရောင်နက်ဗလီ ရှေ့ ဟူစိန်ဘိုင် ဖရဲသီး','ရမ်ဇမ် လအတွက်သာဖွင့်သောဆိုင်ဖြစ်ပါသည်', '16.7888639', '96.1690479', '0','+11111','+11111','+11111', '', '0', '0');
INSERT INTO "public"."shop" ("id", "name_uni", "name_zawgyi", "description","lat", "lon", "menu_id","phone_number_1","phone_number_2","phone_number_3", "address", "township_id", "region_id") VALUES ('4', 'ရောင်နက်ဗလီ ရှေ့ ကဆင်ဘိုင်', 'ရောင်နက်ဗလီ ရှေ့ ကဆင်ဘိုင်','ရမ်ဇမ် လအတွက်သာဖွင့်သောဆိုင်ဖြစ်ပါသည်', '16.7894243', '96.1672589', '0','+11111','+11111','+11111', '', '0', '0' );
INSERT INTO "public"."shop" ("id", "name_uni", "name_zawgyi", "description","lat", "lon", "menu_id","phone_number_1","phone_number_2","phone_number_3", "address", "township_id", "region_id") VALUES ('5', 'ရောင်နက်ဗလီ ရှေ့ ကဆင်ဘိုင်', 'ရောင်နက်ဗလီ ရှေ့ ဇမ်ဇမ်','ရမ်ဇမ် လအတွက်သာဖွင့်သောဆိုင်ဖြစ်ပါသည်', '16.7895347', '96.1684766', '0','+11111','+11111','+11111', '', '0', '0');
INSERT INTO "public"."shop" ("id", "name_uni", "name_zawgyi","description", "lat", "lon", "menu_id","phone_number_1","phone_number_2","phone_number_3", "address", "township_id", "region_id") VALUES ('6', 'ရောင်နက်ဗလီ ရှေ့ ဟူစိန်ဘိုင် ဖရဲသီး', 'ရောင်နက်ဗလီ ရှေ့ ဟူစိန်ဘိုင် ဖရဲသီး','ရမ်ဇမ် လအတွက်သာဖွင့်သောဆိုင်ဖြစ်ပါသည်', '16.7888639', '96.1690479', '0','+11111','+11111','+11111', '', '0', '0' );
INSERT INTO "public"."shop" ("id", "name_uni", "name_zawgyi","description", "lat", "lon", "menu_id","phone_number_1","phone_number_2","phone_number_3", "address", "township_id", "region_id") VALUES ('7', 'ရောင်နက်ဗလီ ရှေ့ ဟူစိန်ဘိုင် ဖရဲသီး', 'ရောင်နက်ဗလီ ရှေ့ ငုံးဆိုင်','ရမ်ဇမ် လအတွက်သာဖွင့်သောဆိုင်ဖြစ်ပါသည်', '16.7888228', '96.1693229', '0','+11111','+11111','+11111', '', '0', '0');
INSERT INTO "public"."shop" ("id", "name_uni", "name_zawgyi","description", "lat", "lon", "menu_id","phone_number_1","phone_number_2","phone_number_3", "address", "township_id", "region_id") VALUES ('8', 'ရောင်နက်ဗလီ ရှေ့ ကဆင်ဘိုင်', 'ရောင်နက်ဗလီ ရှေ့ ကဆင်ဘိုင်','ရမ်ဇမ် လအတွက်သာဖွင့်သောဆိုင်ဖြစ်ပါသည်', '16.7894243', '96.1672589', '0','+11111','+11111','+11111', '', '0', '0' );
INSERT INTO "public"."shop" ("id", "name_uni", "name_zawgyi","description", "lat", "lon", "menu_id","phone_number_1","phone_number_2","phone_number_3", "address", "township_id", "region_id") VALUES ('9', 'ရောင်နက်ဗလီ ရှေ့ ကဆင်ဘိုင်', 'ရောင်နက်ဗလီ ရှေ့ ဇမ်ဇမ်', 'ရမ်ဇမ် လအတွက်သာဖွင့်သောဆိုင်ဖြစ်ပါသည်','16.7895347', '96.1684766', '0','+11111','+11111','+11111', '', '0', '0');
INSERT INTO "public"."shop" ("id", "name_uni", "name_zawgyi","description", "lat", "lon", "menu_id","phone_number_1","phone_number_2","phone_number_3", "address", "township_id", "region_id") VALUES ('10', 'ရောင်နက်ဗလီ ရှေ့ ဟူစိန်ဘိုင် ဖရဲသီး', 'ရောင်နက်ဗလီ ရှေ့ ဟူစိန်ဘိုင် ဖရဲသီး','ရမ်ဇမ် လအတွက်သာဖွင့်သောဆိုင်ဖြစ်ပါသည်', '16.7888639', '96.1690479', '0','+11111','+11111','+11111', '', '0', '0');
INSERT INTO "public"."shop" ("id", "name_uni", "name_zawgyi","description", "lat", "lon", "menu_id","phone_number_1","phone_number_2","phone_number_3", "address", "township_id", "region_id") VALUES ('11', 'ရောင်နက်ဗလီ ရှေ့ ကဆင်ဘိုင်', 'ရောင်နက်ဗလီ ရှေ့ ကဆင်ဘိုင်','ရမ်ဇမ် လအတွက်သာဖွင့်သောဆိုင်ဖြစ်ပါသည်', '16.7894243', '96.1672589', '0','+11111','+11111','+11111', '', '0', '0');
INSERT INTO "public"."shop" ("id", "name_uni", "name_zawgyi","description", "lat", "lon", "menu_id","phone_number_1","phone_number_2","phone_number_3", "address", "township_id", "region_id") VALUES ('12', 'ရောင်နက်ဗလီ ရှေ့ ကဆင်ဘိုင်', 'ရောင်နက်ဗလီ ရှေ့ ဇမ်ဇမ်','ရမ်ဇမ် လအတွက်သာဖွင့်သောဆိုင်ဖြစ်ပါသည်', '16.7895347', '96.1684766', '0','+11111','+11111','+11111', '', '0', '0');
INSERT INTO "public"."shop" ("id", "name_uni", "name_zawgyi","description", "lat", "lon", "menu_id","phone_number_1","phone_number_2","phone_number_3", "address", "township_id", "region_id") VALUES ('13', 'ရောင်နက်ဗလီ ရှေ့ ဟူစိန်ဘိုင် ဖရဲသီး', 'ရောင်နက်ဗလီ ရှေ့ ဟူစိန်ဘိုင် ဖရဲသီး','ရမ်ဇမ် လအတွက်သာဖွင့်သောဆိုင်ဖြစ်ပါသည်', '16.7888639', '96.1690479', '0','+11111','+11111','+11111', '', '0', '0');
INSERT INTO "public"."shop" ("id", "name_uni", "name_zawgyi","description", "lat", "lon", "menu_id","phone_number_1","phone_number_2","phone_number_3", "address", "township_id", "region_id") VALUES ('14', 'ရောင်နက်ဗလီ ရှေ့ ဟူစိန်ဘိုင် ဖရဲသီး', 'ရောင်နက်ဗလီ ရှေ့ ငုံးဆိုင်','ရမ်ဇမ် လအတွက်သာဖွင့်သောဆိုင်ဖြစ်ပါသည်', '16.7888228', '96.1693229', '0','+11111','+11111','+11111', '', '0', '0');

INSERT INTO "public"."shop" ("id", "name_uni", "name_zawgyi","description", "lat", "lon", "menu_id","phone_number_1","phone_number_2","phone_number_3", "address", "township_id", "region_id") VALUES ('15', 'ရောင်နက်ဗလီ ရှေ့ ကဆင်ဘိုင်', 'ရောင်နက်ဗလီ ရှေ့ ကဆင်ဘိုင်','ရမ်ဇမ် လအတွက်သာဖွင့်သောဆိုင်ဖြစ်ပါသည်', '16.7894243', '96.1672589', '0','+11111','+11111','+11111', '', '0', '0');
INSERT INTO "public"."shop" ("id", "name_uni", "name_zawgyi","description", "lat", "lon", "menu_id","phone_number_1","phone_number_2","phone_number_3", "address", "township_id", "region_id") VALUES ('16', 'ရောင်နက်ဗလီ ရှေ့ ကဆင်ဘိုင်', 'ရောင်နက်ဗလီ ရှေ့ ဇမ်ဇမ်','ရမ်ဇမ် လအတွက်သာဖွင့်သောဆိုင်ဖြစ်ပါသည်', '16.7895347', '96.1684766', '0','+11111','+11111','+11111', '', '0', '0');
INSERT INTO "public"."shop" ("id", "name_uni", "name_zawgyi","description", "lat", "lon", "menu_id","phone_number_1","phone_number_2","phone_number_3", "address", "township_id", "region_id") VALUES ('17', 'ရောင်နက်ဗလီ ရှေ့ ဟူစိန်ဘိုင် ဖရဲသီး', 'ရောင်နက်ဗလီ ရှေ့ ဟူစိန်ဘိုင် ဖရဲသီး','ရမ်ဇမ် လအတွက်သာဖွင့်သောဆိုင်ဖြစ်ပါသည်', '16.7888639', '96.1690479', '0','+11111','+11111','+11111', '', '0', '0');
INSERT INTO "public"."shop" ("id", "name_uni", "name_zawgyi","description", "lat", "lon", "menu_id","phone_number_1","phone_number_2","phone_number_3", "address", "township_id", "region_id") VALUES ('18', 'ရောင်နက်ဗလီ ရှေ့ ကဆင်ဘိုင်', 'ရောင်နက်ဗလီ ရှေ့ ကဆင်ဘိုင်','ရမ်ဇမ် လအတွက်သာဖွင့်သောဆိုင်ဖြစ်ပါသည်', '16.7894243', '96.1672589', '0','+11111','+11111','+11111', '', '0', '0');
INSERT INTO "public"."shop" ("id", "name_uni", "name_zawgyi","description", "lat", "lon", "menu_id","phone_number_1","phone_number_2","phone_number_3", "address", "township_id", "region_id") VALUES ('19', 'ရောင်နက်ဗလီ ရှေ့ ကဆင်ဘိုင်', 'ရောင်နက်ဗလီ ရှေ့ ဇမ်ဇမ်','ရမ်ဇမ် လအတွက်သာဖွင့်သောဆိုင်ဖြစ်ပါသည်', '16.7895347', '96.1684766', '0','+11111','+11111','+11111', '', '0', '0');
INSERT INTO "public"."shop" ("id", "name_uni", "name_zawgyi","description", "lat", "lon", "menu_id","phone_number_1","phone_number_2","phone_number_3", "address", "township_id", "region_id") VALUES ('20', 'ရောင်နက်ဗလီ ရှေ့ ဟူစိန်ဘိုင် ဖရဲသီး', 'ရောင်နက်ဗလီ ရှေ့ ဟူစိန်ဘိုင် ဖရဲသီး', 'ရမ်ဇမ် လအတွက်သာဖွင့်သောဆိုင်ဖြစ်ပါသည်','16.7888639', '96.1690479', '0','+11111','+11111','+11111', '', '0', '0');
INSERT INTO "public"."shop" ("id", "name_uni", "name_zawgyi","description", "lat", "lon", "menu_id","phone_number_1","phone_number_2","phone_number_3", "address", "township_id", "region_id") VALUES ('21', 'ရောင်နက်ဗလီ ရှေ့ ဟူစိန်ဘိုင် ဖရဲသီး', 'ရောင်နက်ဗလီ ရှေ့ ငုံးဆိုင်','ရမ်ဇမ် လအတွက်သာဖွင့်သောဆိုင်ဖြစ်ပါသည်', '16.7888228', '96.1693229', '0','+11111','+11111','+11111', '', '0', '0');
INSERT INTO "public"."shop" ("id", "name_uni", "name_zawgyi","description", "lat", "lon", "menu_id","phone_number_1","phone_number_2","phone_number_3", "address", "township_id", "region_id") VALUES ('22', 'ရောင်နက်ဗလီ ရှေ့ ကဆင်ဘိုင်', 'ရောင်နက်ဗလီ ရှေ့ ကဆင်ဘိုင်','ရမ်ဇမ် လအတွက်သာဖွင့်သောဆိုင်ဖြစ်ပါသည်', '16.7894243', '96.1672589', '0','+11111','+11111','+11111', '', '0', '0');
INSERT INTO "public"."shop" ("id", "name_uni", "name_zawgyi","description", "lat", "lon", "menu_id","phone_number_1","phone_number_2","phone_number_3", "address", "township_id", "region_id") VALUES ('23', 'ရောင်နက်ဗလီ ရှေ့ ကဆင်ဘိုင်', 'ရောင်နက်ဗလီ ရှေ့ ဇမ်ဇမ်', 'ရမ်ဇမ် လအတွက်သာဖွင့်သောဆိုင်ဖြစ်ပါသည်','16.7895347', '96.1684766', '0','+11111','+11111','+11111', '', '0', '0');
INSERT INTO "public"."shop" ("id", "name_uni", "name_zawgyi","description", "lat", "lon", "menu_id","phone_number_1","phone_number_2","phone_number_3", "address", "township_id", "region_id") VALUES ('24', 'ရောင်နက်ဗလီ ရှေ့ ဟူစိန်ဘိုင် ဖရဲသီး', 'ရောင်နက်ဗလီ ရှေ့ ဟူစိန်ဘိုင် ဖရဲသီး', 'ရမ်ဇမ် လအတွက်သာဖွင့်သောဆိုင်ဖြစ်ပါသည်','16.7888639', '96.1690479', '0','+11111','+11111','+11111', '', '0', '0');
INSERT INTO "public"."shop" ("id", "name_uni", "name_zawgyi","description", "lat", "lon", "menu_id","phone_number_1","phone_number_2","phone_number_3", "address", "township_id", "region_id") VALUES ('25', 'ရောင်နက်ဗလီ ရှေ့ ကဆင်ဘိုင်', 'ရောင်နက်ဗလီ ရှေ့ ကဆင်ဘိုင်','ရမ်ဇမ် လအတွက်သာဖွင့်သောဆိုင်ဖြစ်ပါသည်', '16.7894243', '96.1672589', '0','+11111','+11111','+11111', '', '0', '0');
INSERT INTO "public"."shop" ("id", "name_uni", "name_zawgyi","description", "lat", "lon", "menu_id","phone_number_1","phone_number_2","phone_number_3", "address", "township_id", "region_id") VALUES ('26', 'ရောင်နက်ဗလီ ရှေ့ ကဆင်ဘိုင်', 'ရောင်နက်ဗလီ ရှေ့ ဇမ်ဇမ်', 'ရမ်ဇမ် လအတွက်သာဖွင့်သောဆိုင်ဖြစ်ပါသည်','16.7895347', '96.1684766', '0','+11111','+11111','+11111', '', '0', '0');
INSERT INTO "public"."shop" ("id", "name_uni", "name_zawgyi","description", "lat", "lon", "menu_id","phone_number_1","phone_number_2","phone_number_3", "address", "township_id", "region_id") VALUES ('27', 'ရောင်နက်ဗလီ ရှေ့ ဟူစိန်ဘိုင် ဖရဲသီး', 'ရောင်နက်ဗလီ ရှေ့ ဟူစိန်ဘိုင် ဖရဲသီး','ရမ်ဇမ် လအတွက်သာဖွင့်သောဆိုင်ဖြစ်ပါသည်', '16.7888639', '96.1690479', '0','+11111','+11111','+11111', '', '0', '0');
INSERT INTO "public"."shop" ("id", "name_uni", "name_zawgyi","description", "lat", "lon", "menu_id","phone_number_1","phone_number_2","phone_number_3", "address", "township_id", "region_id") VALUES ('28', 'ရောင်နက်ဗလီ ရှေ့ ဟူစိန်ဘိုင် ဖရဲသီး', 'ရောင်နက်ဗလီ ရှေ့ ငုံးဆိုင်','ရမ်ဇမ် လအတွက်သာဖွင့်သောဆိုင်ဖြစ်ပါသည်', '16.7888228', '96.1693229', '0','+11111','+11111','+11111', '', '0', '0');