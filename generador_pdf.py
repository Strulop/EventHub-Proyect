from fpdf import FPDF
from io import BytesIO
import os

# Clase personalizada para el PDF
class PDF(FPDF):
    def header(self):
        icon_path = os.path.join("static", "img", "favicon.png")
        self.image(icon_path, x=10, y=8, w=20)
        self.set_xy(7, 8)
        # Logo o nombre de la empresa
        self.set_font("Helvetica", 'B', 16)
        self.set_text_color(145, 115, 244)  
        self.cell(0, 10, "EventHub", ln=True, align="C")
        self.set_font("Helvetica", '', 12)
        self.cell(0, 10, "Ticket de Compra", ln=True, align="C")
        # Línea divisoria
        self.set_draw_color(145, 115, 244)
        self.set_line_width(0.5)
        self.line(10, 30, self.w - 10, 30)
        self.ln(10)

    def footer(self):
        # Pie de página centrado en gris
        self.set_y(-20)
        self.set_text_color(100, 100, 100)
        self.set_font("Helvetica", 'I', 10)
        self.cell(0, 10, "Gracias por su compra!", align="C")


def generate_ticket_pdf(evento, quantity, event_price, subtotal, fees, total, buyer_email):
    """
    Genera el PDF del ticket de compra y retorna un objeto BytesIO.
    """
    pdf = PDF()
    pdf.add_page()
    
    # Bloque principal con diseño moderno
    # Título Principal con Fondo Corporativo
    pdf.set_fill_color(145, 115, 244)  
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", 'B', 18)
    pdf.cell(0, 12, "TICKET DE COMPRA", ln=1, align="C", fill=True)
    pdf.ln(5)
    
    # Bloque de Información del Evento
    x = 10
    w = pdf.w - 20
    y = pdf.get_y()
    h = 40  # Altura del bloque (ajustable)
    pdf.set_fill_color(246,207,254)  
    pdf.rect(x, y, w, h, style='F')     # Dibujar el rectángulo
    
    pdf.set_xy(x + 5, y + 5)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(40, 8, "Evento:")
    pdf.set_font("Helvetica", '', 12)
    pdf.cell(0, 8, f"{evento['nombre']}", ln=1)
    
    pdf.set_xy(x + 5, pdf.get_y())
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(40, 8, "Fecha:")
    pdf.set_font("Helvetica", '', 12)
    pdf.cell(0, 8, f"{evento['fecha']}", ln=1)
    
    pdf.set_xy(x + 5, pdf.get_y())
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(40, 8, "Categoría:")
    pdf.set_font("Helvetica", '', 12)
    pdf.cell(0, 8, f"{evento['categoria']}", ln=1)
    
    pdf.set_xy(x + 5, pdf.get_y())
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(40, 8, "Ubicación:")
    pdf.set_font("Helvetica", '', 12)
    pdf.cell(0, 8, f"{evento['ubicacion']}", ln=1)
    pdf.ln(5)
    
    # Bloque de Detalles de Compra
    y = pdf.get_y()
    h = 45  # Altura del bloque (ajustable)
    pdf.set_fill_color(226,207,254)
    pdf.rect(x, y, w, h, style='F')
    
    pdf.set_xy(x + 5, y + 5)
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(55, 8, "Cantidad de tickets:")
    pdf.set_font("Helvetica", '', 12)
    pdf.cell(0, 8, f"{quantity}", ln=1)
    
    pdf.set_xy(x + 5, pdf.get_y())
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(55, 8, "Precio por ticket:")
    pdf.set_font("Helvetica", '', 12)
    pdf.cell(0, 8, f"${event_price:.2f}", ln=1)
    
    pdf.set_xy(x + 5, pdf.get_y())
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(55, 8, "Subtotal:")
    pdf.set_font("Helvetica", '', 12)
    pdf.cell(0, 8, f"${subtotal:.2f}", ln=1)
    
    pdf.set_xy(x + 5, pdf.get_y())
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(55, 8, "Gastos de gestión:")
    pdf.set_font("Helvetica", '', 12)
    pdf.cell(0, 8, f"${fees:.2f}", ln=1)
    
    pdf.set_xy(x + 5, pdf.get_y())
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(55, 8, "Total:")
    pdf.set_text_color(145, 115, 244)  # Azul para resaltar
    pdf.cell(0, 8, f"${total:.2f}", ln=1)
    
    pdf.set_text_color(0, 0, 0)  # Volver a negro
    pdf.ln(5)
    
    # Bloque de Información del Comprador
    y = pdf.get_y()
    h = 15
    pdf.set_fill_color(245, 245, 245)
    pdf.rect(x, y, w, h, style='F')
    
    pdf.set_xy(x + 5, y + 4)
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(40, 8, "Comprador:")
    pdf.set_font("Helvetica", '', 12)
    pdf.cell(0, 8, f"{buyer_email}", ln=1)
    pdf.ln(5)
    
    # Bloque de Política de Devoluciones
    y = pdf.get_y()
    h = 20  # Altura ajustable según el texto
    pdf.set_fill_color(255, 255, 255)
    pdf.rect(x, y, w, h, style='F')
    
    pdf.set_xy(x + 5, y + 4)
    pdf.set_font("Helvetica", 'I', 10)
    pdf.set_text_color(150, 0, 0)  # Rojo suave para alertar
    pdf.multi_cell(0, 5, "Politica de Devoluciones: Las entradas no son reembolsables. Se permite cambio de titular hasta 48 horas antes del evento.", border=0)
    pdf.ln(5)
    
    # Generar el contenido del PDF como string y envolverlo en BytesIO
    pdf_content = pdf.output(dest='S')
    pdf_bytes = pdf_content.encode('latin1', errors='replace')
    pdf_buffer = BytesIO(pdf_bytes)
    pdf_buffer.seek(0)
    return pdf_buffer
