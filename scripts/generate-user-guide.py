#!/usr/bin/env python3
"""دليل استخدام احترافي لبرنامج إعداد دراسات الجدوى"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak,
    Image, ListFlowable, ListItem, HRFlowable, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.frames import Frame
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
import os

# تسجيل الخطوط العربية
pdfmetrics.registerFont(TTFont('Cairo', '/usr/share/fonts/truetype/noto-serif-sc/NotoSerifSC-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Cairo-Bold', '/usr/share/fonts/truetype/noto-serif-sc/NotoSerifSC-Bold.ttf'))

# الألوان
PRIMARY = HexColor('#0d9488')
ACCENT = HexColor('#facc15')
DARK = HexColor('#1f2937')
LIGHT = HexColor('#f3f4f6')
MUTED = HexColor('#6b7280')
SUCCESS = HexColor('#10b981')
WHITE = white

# الأنماط
styles = getSampleStyleSheet()

style_title = ParagraphStyle('Title', parent=styles['Title'],
    fontName='Cairo-Bold', fontSize=28, textColor=PRIMARY, alignment=TA_CENTER, spaceAfter=10)

style_subtitle = ParagraphStyle('Subtitle', parent=styles['Normal'],
    fontName='Cairo', fontSize=14, textColor=MUTED, alignment=TA_CENTER, spaceAfter=20)

style_h1 = ParagraphStyle('H1', parent=styles['Heading1'],
    fontName='Cairo-Bold', fontSize=18, textColor=PRIMARY, spaceAfter=10, spaceBefore=20)

style_h2 = ParagraphStyle('H2', parent=styles['Heading2'],
    fontName='Cairo-Bold', fontSize=14, textColor=DARK, spaceAfter=8, spaceBefore=15)

style_body = ParagraphStyle('Body', parent=styles['Normal'],
    fontName='Cairo', fontSize=11, textColor=DARK, alignment=TA_JUSTIFY, spaceAfter=8, leading=18)

style_bullet = ParagraphStyle('Bullet', parent=style_body,
    leftIndent=20, bulletIndent=10, spaceAfter=4)

style_note = ParagraphStyle('Note', parent=style_body,
    fontSize=10, textColor=MUTED, leftIndent=15, spaceAfter=6)

style_table_header = ParagraphStyle('TableHeader', parent=styles['Normal'],
    fontName='Cairo-Bold', fontSize=10, textColor=WHITE, alignment=TA_CENTER)

style_table_cell = ParagraphStyle('TableCell', parent=styles['Normal'],
    fontName='Cairo', fontSize=9, textColor=DARK, alignment=TA_CENTER)

# === دالة إنشاء الصفحات ===
def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont('Cairo', 9)
    canvas.setFillColor(MUTED)
    canvas.drawCentredString(A4[0] / 2, 1.5 * cm, str(doc.page))
    canvas.restoreState()

# === المحتوى ===
story = []

# === صفحة الغلاف ===
story.append(Spacer(1, 8 * cm))
story.append(Paragraph('دليل استخدام برنامج<br/>إعداد دراسات الجدوى', style_title))
story.append(Spacer(1, 1 * cm))
story.append(HRFlowable(width='60%', thickness=2, color=ACCENT, hAlign='CENTER'))
story.append(Spacer(1, 1 * cm))
story.append(Paragraph('النظام المتكامل لإعداد دراسات الجدوى الاقتصادية', style_subtitle))
story.append(Spacer(1, 3 * cm))

# معلومات
info_data = [
    ['الإصدار', '1.0.0'],
    ['التاريخ', '2026'],
    ['العملة الرئيسية', 'الريال اليمني (YER)'],
    ['اللغات', 'العربية / الإنجليزية'],
]
info_table = Table(info_data, colWidths=[5 * cm, 7 * cm])
info_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), 'Cairo'),
    ('FONTSIZE', (0, 0), (-1, -1), 11),
    ('TEXTCOLOR', (0, 0), (0, -1), MUTED),
    ('TEXTCOLOR', (1, 0), (1, -1), DARK),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('LINEBELOW', (0, 0), (-1, -1), 0.5, LIGHT),
]))
story.append(info_table)
story.append(PageBreak())

# === جدول المحتويات ===
story.append(Paragraph('جدول المحتويات', style_h1))
story.append(HRFlowable(width='100%', thickness=2, color=PRIMARY))
story.append(Spacer(1, 0.5 * cm))

toc_items = [
    '1. مقدمة عن البرنامج',
    '2. الواجهة الرئيسية والقوائم',
    '3. إنشاء مشروع جديد',
    '4. الدراسات الثمانية',
    '5. النتائج والتقارير',
    '6. المكتبات المرجعية',
    '7. التحليلات المتقدمة',
    '8. الإعدادات والثيمات',
    '9. التصدير والاستيراد',
    '10. التثبيت كبرنامج مكتبي',
    '11. الأسئلة الشائعة',
]

for item in toc_items:
    story.append(Paragraph(item, style_body))
    story.append(Spacer(1, 4))

story.append(PageBreak())

# === 1. مقدمة ===
story.append(Paragraph('1. مقدمة عن البرنامج', style_h1))
story.append(HRFlowable(width='100%', thickness=1, color=LIGHT))
story.append(Spacer(1, 0.3 * cm))

story.append(Paragraph(
    'برنامج إعداد دراسات الجدوى هو نظام متكامل لإعداد دراسات الجدوى الاقتصادية '
    'بشكل احترافي ومتكامل. يدعم البرنامج جميع أنواع المشاريع: الزراعية والصناعية '
    'والخدمية ومشاريع الطاقة المتجددة. يعتمد البرنامج الريال اليمني كعملة رئيسية '
    'مع إمكانية التبديل بين 10 عملات مختلفة، ويدعم اللغتين العربية والإنجليزية.',
    style_body))

story.append(Paragraph('الميزات الرئيسية:', style_h2))

features = [
    '8 دراسات متكاملة (تأسيس، اجتماعية، بيئية، قانونية، تسويقية، فنية، مالية، اقتصادية)',
    '24 نافذة منبثقة (Dialog) لكل عمليات البرنامج',
    '34 محصول زراعي يمني بمواصفات علمية كاملة',
    '30 مصنع تحويلي ببيانات اقتصادية تفصيلية',
    '10 مشاريع طاقة متجددة + 4 حاسبات متخصصة',
    '12 مشروع نموذجي كامل قابل للتحميل والتحرير',
    'مساعد ذكي محادثة للأسئلة الفورية',
    'محاكاة Monte Carlo لتحليل المخاطر الكمي',
    'تحليل SWOT وقوى Porter الخمس',
    'إدارة مخاطر مع مصفوفة حرارية',
    'تتبع مراحل التنفيذ مع مخطط Gantt',
    '8 ثيمات قابلة للتخصيص + 4 أوضاع عرض',
    'خريطة موقع المشروع (OpenStreetMap)',
    'أسعار صرف حية من API مجاني',
    'PWA قابل للتثبيت كبرنامج مكتبي',
]

for f in features:
    story.append(Paragraph(f'• {f}', style_bullet))

story.append(PageBreak())

# === 2. الواجهة الرئيسية ===
story.append(Paragraph('2. الواجهة الرئيسية والقوائم', style_h1))
story.append(HRFlowable(width='100%', thickness=1, color=LIGHT))
story.append(Spacer(1, 0.3 * cm))

story.append(Paragraph(
    'يتكون البرنامج من شريط قوائم علوي يحتوي على 4 قوائم رئيسية وأزرار سريعة. '
    'يحتوي أيضاً على شريط أقسام سفلي للتنقل السريع بين الأقسام المختلفة.',
    style_body))

story.append(Paragraph('القوائم الرئيسية:', style_h2))

menus_data = [
    [Paragraph('القائمة', style_table_header), Paragraph('الوصف', style_table_header)],
    [Paragraph('ملف', style_table_cell), Paragraph('مشروع جديد، فح، حفظ، تصدير، استيراد، مقارنة، نسخ احتياطي', style_table_cell)],
    [Paragraph('عرض', style_table_cell), Paragraph('اللغة، العملة، أسعار الصرف، الإعدادات، أوضاع العرض', style_table_cell)],
    [Paragraph('الدراسات', style_table_cell), Paragraph('تنقل سريع بين الأقسام الثمانية', style_table_cell)],
    [Paragraph('مساعدة', style_table_cell), Paragraph('دليل، قاموس مصطلحات، مشاريع نموذجية، مكتبات', style_table_cell)],
]

menus_table = Table(menus_data, colWidths=[3 * cm, 12 * cm])
menus_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
    ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
    ('FONTNAME', (0, 0), (-1, -1), 'Cairo'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 0.5, LIGHT),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT]),
]))
story.append(menus_table)
story.append(Spacer(1, 0.5 * cm))

story.append(Paragraph('الأزرار السريعة:', style_h2))
quick_buttons = [
    '🧭 تنقل - نافذة تنقل سريع بين الأقسام',
    '🔔 إشعارات - إشعارات ذكية عن المشاريع',
    'ℹ️ معلومات - معلومات شاملة عن المشروع الحالي',
    '📜 نسخ - سجل النسخ + مشاركة المشروع',
    '🌓 وضع - تبديل أوضاع العرض (فاتح/داكن/تلقائي/قراءة)',
    '⌨️ Ctrl+K - لوحة أوامر سريعة للبحث',
    '🤖 مساعد ذكي - محادثة للأسئلة الفورية',
]
for b in quick_buttons:
    story.append(Paragraph(f'• {b}', style_bullet))

story.append(PageBreak())

# === 3. إنشاء مشروع ===
story.append(Paragraph('3. إنشاء مشروع جديد', style_h1))
story.append(HRFlowable(width='100%', thickness=1, color=LIGHT))
story.append(Spacer(1, 0.3 * cm))

story.append(Paragraph(
    'لإنشاء مشروع جديد، اتبع الخطوات التالية:',
    style_body))

steps = [
    '1. من قائمة "ملف"، اختر "مشروع جديد" أو اضغط Ctrl+N',
    '2. اختر بين "من قالب جاهز" أو "مشروع فارغ"',
    '3. إذا اخترت قالباً، تصفح القوالب المتاحة (8 قوالب)',
    '4. أدخل اسم المشروع والوصف',
    '5. اختر عملة العرض (الافتراضية: الريال اليمني)',
    '6. اضغط "حفظ" لإنشاء المشروع',
    '7. سيتم نقلك تلقائياً لقسم "تأسيس المشروع" لبدء الإدخال',
]

for s in steps:
    story.append(Paragraph(s, style_bullet))

story.append(Spacer(1, 0.3 * cm))
story.append(Paragraph(
    'يمكنك أيضاً تحميل مشروع نموذجي جاهز من قسم "مشاريع نموذجية" '
    'في الشريط العلوي. يتوفر 12 مشروع نموذجي كامل قابل للتحرير.',
    style_body))

story.append(PageBreak())

# === 4. الدراسات الثمانية ===
story.append(Paragraph('4. الدراسات الثمانية', style_h1))
story.append(HRFlowable(width='100%', thickness=1, color=LIGHT))
story.append(Spacer(1, 0.3 * cm))

story.append(Paragraph(
    'يتضمن البرنامج ثماني دراسات متكاملة تشكل دراسة الجدوى الكاملة. '
    'كل دراسة تحتوي على نموذج إدخال شامل مع حفظ تلقائي للبيانات.',
    style_body))

studies_data = [
    [Paragraph('الدراسة', style_table_header), Paragraph('المحتوى الرئيسي', style_table_header)],
    [Paragraph('تأسيس المشروع', style_table_cell), Paragraph('الاسم، النوع، الموقع، المالك، رأس المال، المدة', style_table_cell)],
    [Paragraph('الدراسة الاجتماعية', style_table_cell), Paragraph('الوظائف، التدريب، الأثر المجتمعي', style_table_cell)],
    [Paragraph('الدراسة البيئية', style_table_cell), Paragraph('الانبعاثات، المياه، النفايات، التخفيف', style_table_cell)],
    [Paragraph('الدراسة القانونية', style_table_cell), Paragraph('التراخيص، القوانين، العقود، التأمين', style_table_cell)],
    [Paragraph('الدراسة التسويقية', style_table_cell), Paragraph('العملاء، المنافسون، التسعير، التوزيع', style_table_cell)],
    [Paragraph('الدراسة الفنية', style_table_cell), Paragraph('الطاقة، المعدات، المواد الخام، الجودة', style_table_cell)],
    [Paragraph('الدراسة المالية', style_table_cell), Paragraph('استثمار، أصول، قروض، تدفق نقدي سنوي', style_table_cell)],
    [Paragraph('الدراسة الاقتصادية', style_table_cell), Paragraph('معدل الخصم، تحليل المخاطر، الحساسية', style_table_cell)],
]

studies_table = Table(studies_data, colWidths=[4 * cm, 11 * cm])
studies_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
    ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
    ('FONTNAME', (0, 0), (-1, -1), 'Cairo'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('GRID', (0, 0), (-1, -1), 0.5, LIGHT),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT]),
]))
story.append(studies_table)

story.append(PageBreak())

# === 5. النتائج والتقارير ===
story.append(Paragraph('5. النتائج والتقارير', style_h1))
story.append(HRFlowable(width='100%', thickness=1, color=LIGHT))
story.append(Spacer(1, 0.3 * cm))

story.append(Paragraph(
    'صفحة "النتائج والتقارير" هي القلب التحليلي للبرنامج. تحتوي على جميع '
    'المؤشرات والرسوم البيانية والتحليلات المتقدمة.',
    style_body))

story.append(Paragraph('المؤشرات المالية:', style_h2))
indicators = [
    'NPV (صافي القيمة الحالية) - يجب أن يكون موجباً',
    'IRR (معدل العائد الداخلي) - يجب أن يتجاوز معدل الخصم',
    'MIRR (معدل العائد الداخلي المعدّل)',
    'ROI (العائد على الاستثمار)',
    'فترة الاسترداد + فترة الاسترداد المخصومة',
    'مؤشر الربحية (PI)',
    'WACC (متوسط تكلفة رأس المال)',
    'هامش الأمان',
]
for ind in indicators:
    story.append(Paragraph(f'• {ind}', style_bullet))

story.append(Paragraph('التحليلات المتقدمة:', style_h2))
analysis = [
    'محاكاة Monte Carlo (1000+ سيناريو عشوائي)',
    'مخطط Tornado (تحليل حساسية مرئي)',
    'تحليل السيناريوهات (متفائل/متعادل/متشائم)',
    'تحليل SWOT التفاعلي',
    'قوى Porter الخمس',
    'إدارة المخاطر مع مصفوفة حرارية',
    'تتبع مراحل التنفيذ (Gantt)',
    'لوحة KPIs التنفيذية',
    'تحليل نقطة التعادل',
    'حاسبة الاستدامة البيئية',
    'خريطة موقع المشروع',
    'مساعد ذكي محادثة',
]
for a in analysis:
    story.append(Paragraph(f'• {a}', style_bullet))

story.append(PageBreak())

# === 6. المكتبات المرجعية ===
story.append(Paragraph('6. المكتبات المرجعية', style_h1))
story.append(HRFlowable(width='100%', thickness=1, color=LIGHT))
story.append(Spacer(1, 0.3 * cm))

story.append(Paragraph(
    'يحتوي البرنامج على مكتبات مرجعية شاملة يمكن الوصول إليها من قائمة "مساعدة":',
    style_body))

libs = [
    ('مكتبة المحاصيل اليمنية', '34 محصول بمواصفات علمية كاملة + مقارنة + توصية حسب الموقع'),
    ('مكتبة مصانع الصناعات التحويلية', '30 مصنع ببيانات اقتصادية + ترتيب حسب الربحية'),
    ('مكتبة مشاريع الطاقة المتجددة', '10 مشاريع + 4 حاسبات (شمسية/رياح/كهروماء/تعرفة)'),
    ('قاموس المصطلحات المالية', '28 مصطلح مالي واقتصادي مع تعريفات وصيغ'),
    ('مشاريع نموذجية', '12 مشروع كامل قابل للتحميل والتحرير والتصدير والمقارنة'),
]

for name, desc in libs:
    story.append(Paragraph(f'<b>{name}</b>', style_h2))
    story.append(Paragraph(desc, style_body))

story.append(PageBreak())

# === 7. التصدير والاستيراد ===
story.append(Paragraph('7. التصدير والاستيراد', style_h1))
story.append(HRFlowable(width='100%', thickness=1, color=LIGHT))
story.append(Spacer(1, 0.3 * cm))

story.append(Paragraph('صيغ التصدير المتاحة:', style_h2))

export_data = [
    [Paragraph('الصيغة', style_table_header), Paragraph('الاستخدام', style_table_header)],
    [Paragraph('PDF', style_table_cell), Paragraph('تقرير احترافي للطباعة', style_table_cell)],
    [Paragraph('PowerPoint', style_table_cell), Paragraph('عرض تقديمي للمستثمرين', style_table_cell)],
    [Paragraph('Word', style_table_cell), Paragraph('قالب احترافي قابل للتحرير', style_table_cell)],
    [Paragraph('Excel', style_table_cell), Paragraph('ملف XLSX بـ 9 أوراق', style_table_cell)],
    [Paragraph('JSON', style_table_cell), Paragraph('نسخة احتياطية كاملة', style_table_cell)],
    [Paragraph('HTML', style_table_cell), Paragraph('صفحة ويب للمعاينة', style_table_cell)],
    [Paragraph('CSV', style_table_cell), Paragraph('استيراد مشاريع متعددة', style_table_cell)],
]

export_table = Table(export_data, colWidths=[3 * cm, 12 * cm])
export_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
    ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
    ('FONTNAME', (0, 0), (-1, -1), 'Cairo'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('GRID', (0, 0), (-1, -1), 0.5, LIGHT),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT]),
]))
story.append(export_table)

story.append(Spacer(1, 0.3 * cm))
story.append(Paragraph(
    'يدعم البرنامج أيضاً استيراد المشاريع من ملفات Excel و CSV، '
    'وكذلك النسخ الاحتياطي الكامل لجميع المشاريع.',
    style_body))

story.append(PageBreak())

# === 8. التثبيت كبرنامج مكتبي ===
story.append(Paragraph('8. التثبيت كبرنامج مكتبي', style_h1))
story.append(HRFlowable(width='100%', thickness=1, color=LIGHT))
story.append(Spacer(1, 0.3 * cm))

story.append(Paragraph(
    'البرنامج هو تطبيق ويب تقدمي (PWA) يمكن تثبيته كبرنامج مكتبي على '
    'نظام Windows. هذا يعطيه مظهر وسلوك برنامج مكتبي حقيقي مع نافذة '
    'مستقلة وأيقونة على سطح المكتب.',
    style_body))

story.append(Paragraph('خطوات التثبيت على Windows:', style_h2))

install_steps = [
    '1. افتح البرنامج في متصفح Google Chrome أو Microsoft Edge',
    '2. انتظر تحميل البرنامج بالكامل',
    '3. ابحث عن أيقونة "تثبيت" في شريط العنوان (⊕)',
    '4. اضغط على أيقونة التثبيت',
    '5. اضغط "تثبيت" في النافذة المنبثقة',
    '6. سيظهر البرنامج في قائمة Start وعلى سطح المكتب',
    '7. افتحه مثل أي برنامج مكتبي آخر',
]

for s in install_steps:
    story.append(Paragraph(s, style_bullet))

story.append(Spacer(1, 0.3 * cm))
story.append(Paragraph('مزايا التثبيت كـ PWA:', style_h2))
pwa_adv = [
    'يعمل في نافذة مستقلة بدون شريط المتصفح',
    'أيقونة على سطح المكتب وقائمة Start',
    'تحديثات تلقائية بدون إعادة تثبيت',
    'يعمل بدون إنترنت (Offline Mode)',
    'أداء أسرع من المتصفح',
    'لا يحتاج تثبيت تقليدي (.exe)',
]
for a in pwa_adv:
    story.append(Paragraph(f'• {a}', style_bullet))

story.append(PageBreak())

# === 9. الإعدادات والثيمات ===
story.append(Paragraph('9. الإعدادات والثيمات', style_h1))
story.append(HRFlowable(width='100%', thickness=1, color=LIGHT))
story.append(Spacer(1, 0.3 * cm))

story.append(Paragraph('الثيمات المتاحة:', style_h2))
themes = [
    'فيروزي كلاسيكي (الافتراضي)',
    'ملكي أزرق',
    'صحراوي برتقالي',
    'غابي أخضر',
    'ليلي داكن',
    'ذهبي فاخر',
    'مرجاني وردي',
    'رمادي احترافي',
]
for t in themes:
    story.append(Paragraph(f'• {t}', style_bullet))

story.append(Paragraph('أوضاع العرض:', style_h2))
modes = [
    '☀️ فاتح - الوضع الافتراضي',
    '🌙 داكن - للإضاءة المنخفضة',
    '🖥️ تلقائي - يتبع تفضيلات النظام',
    '📖 قراءة - خلفية دافئة + خط أكبر',
]
for m in modes:
    story.append(Paragraph(f'• {m}', style_bullet))

story.append(Paragraph('الإعدادات الأخرى:', style_h2))
other_settings = [
    'اسم المؤسسة + شعار (يظهر في التقارير)',
    'ترويسة وتذييل مخصصان',
    'معدل خصم افتراضي',
    'معدل VAT وضريبة الدخل الافتراضية',
    'حجم الخط (صغير/متوسط/كبير)',
    'أسعار صرف حية من API مجاني',
]
for s in other_settings:
    story.append(Paragraph(f'• {s}', style_bullet))

story.append(PageBreak())

# === 10. الأسئلة الشائعة ===
story.append(Paragraph('10. الأسئلة الشائعة', style_h1))
story.append(HRFlowable(width='100%', thickness=1, color=LIGHT))
story.append(Spacer(1, 0.3 * cm))

faq_items = [
    ('س: هل يعمل البرنامج بدون إنترنت؟',
     'ج: نعم، البرنامج PWA ويدعم Offline Mode. البيانات تُحفظ محلياً.'),
    ('س: هل يمكنني تغيير العملة؟',
     'ج: نعم، من قائمة "عرض ← العملة" أو Ctrl+K ثم ابحث عن العملة.'),
    ('س: هل يمكنني تصدير التقرير بصيغة Word؟',
     'ج: نعم، من قائمة "ملف ← تصدير ← Word". القالب احترافي وقابل للتحرير.'),
    ('س: هل يدعم البرنامج اللغة الإنجليزية؟',
     'ج: نعم، من قائمة "عرض ← اللغة" يمكن التبديل بين العربي والإنجليزي.'),
    ('س: كيف أحفظ نسخة من المشروع؟',
     'ج: استخدم زر "النسخ والمشاركة" (📜) لحفظ لقطة + مشاركة الرابط.'),
    ('س: هل يمكنني مقارنة عدة مشاريع؟',
     'ج: نعم، من قائمة "ملف ← مقارنة المشاريع" أو في صفحة المشاريع النموذجية.'),
    ('س: كيف أحصل على أسعار صرف حية؟',
     'ج: من "عرض ← تعديل أسعار الصرف ← أسعار حية".'),
    ('س: هل يمكنني استخدام البرنامج على الموبايل؟',
     'ج: نعم، البرنامج متجاوب تماماً مع قائمة سفلية للموبايل.'),
]

for q, a in faq_items:
    story.append(Paragraph(f'<b>{q}</b>', style_body))
    story.append(Paragraph(a, style_note))
    story.append(Spacer(1, 0.2 * cm))

story.append(Spacer(1, 1 * cm))
story.append(HRFlowable(width='100%', thickness=1, color=LIGHT))
story.append(Spacer(1, 0.3 * cm))
story.append(Paragraph(
    'للمزيد من المساعدة، استخدم المساعد الذكي 🤖 في الزاوية السفلية، '
    'أو اضغط F1 لفتح دليل الاستخدام السريع.',
    style_note))

# === إنشاء PDF ===
output_path = '/home/z/my-project/download/دليل-الاستخدام-احترافي.pdf'

doc = SimpleDocTemplate(
    output_path,
    pagesize=A4,
    rightMargin=2 * cm,
    leftMargin=2 * cm,
    topMargin=2.5 * cm,
    bottomMargin=2.5 * cm,
    title='دليل استخدام برنامج إعداد دراسات الجدوى',
    author='Z.ai',
    subject='دليل استخدام احترافي',
    creator='برنامج إعداد دراسات الجدوى',
)

doc.build(story, onFirstPage=lambda c, d: None, onLaterPages=add_page_number)

print(f"✅ PDF generated: {output_path}")
print(f"   Size: {os.path.getsize(output_path) / 1024:.1f} KB")
