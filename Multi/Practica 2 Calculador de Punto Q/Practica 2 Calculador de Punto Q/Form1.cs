using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

// APLICACION CREADA POR: - KEBERLEIN GIAN - PALETTA LAUTARO
// APLICACION CREADA POR: - KEBERLEIN GIAN - PALETTA LAUTARO
// APLICACION CREADA POR: - KEBERLEIN GIAN - PALETTA LAUTARO

namespace Practica_2_Calculador_de_Punto_Q
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void Btn_calcular_Click(object sender, EventArgs e)
        {

            // Obtenemos los valores en Ohms
            double vcc = double.Parse(txt_vcc.Text);
            double rc = Calculos.Verificar(txt_rc.Text, cmb_rc.Text);
            double re = Calculos.Verificar(txt_re.Text, cmb_re.Text);
            double rb = Calculos.Verificar(txt_rb.Text, cmb_rb.Text);
            double hfe = double.Parse(txt_hfe.Text);

            // Calculamos el punto Q
            double[] PuntoQ = Calculos.PuntoQ(vcc, hfe, rb, rc, re);

            // Convertimos a unos pocos decimales
            PuntoQ[0] = Math.Truncate(PuntoQ[0] * 10000000) / 10000000;
            PuntoQ[1] = Math.Truncate(PuntoQ[1] * 10000000) / 10000000;

            // Mostramos los valores de el punto Q en notacion cientifica
            lbl_icq.Text = Calculos.Notacion(PuntoQ[0], "A");
            lbl_vceq.Text = Calculos.Notacion(PuntoQ[1], "V");

            // Llamamos a la funcion graficar pasandole los valores de Q, vcc e ICMax
            Graficar(PuntoQ[0], PuntoQ[1],PuntoQ[2], PuntoQ[3]);
        }

        void Graficar(double icq, double vceq, double icmax, double vcc)
        {
            // Declaramos nuestro grafico y lo limpiamos antes de graficar
            Graphics grafico;
            grafico = pictureBox1.CreateGraphics();
            grafico.Clear(Color.White);
            
            // Establecemos nuestro (0, 0) en el grafico y la escala
            int x0 = 20;
            int y0 = pictureBox1.Height - 20;
            int lineas_div = 20;

            grafico.TranslateTransform(x0, y0);
            grafico.ScaleTransform(1, -1);

            // Creamos los objetos con los que vamos a dibujar
            Pen lapiz = new Pen(Color.Black, 2);
            SolidBrush myBrush = new SolidBrush(Color.Black);

            //Dibujamos los ejes del grafico
            grafico.DrawLine(lapiz, -10, 0, pictureBox1.Width, 0);
            grafico.DrawLine(lapiz, 0, -10, 0, pictureBox1.Height);

            //Dibujamos las lineas divisorias del grafico
            for (int i = lineas_div; i < pictureBox1.Width; i += lineas_div)
            {
                grafico.DrawLine(lapiz, i, 5, i, -5);
                grafico.DrawLine(lapiz, -5, i, 5, i);
            }

            //Dibujamos la recta de carga por defecto de 10 divisiones x 10 divisiones
            grafico.DrawLine(lapiz, 0, 10 * lineas_div, 10 * lineas_div, 0);

            //Establecemos la escala por division en Amper y Volt teniendo en cuenta que hay solo 10 divisiones
            float ADiv = Convert.ToSingle(icmax / 10);
            float VDiv = Convert.ToSingle(vcc / 10);

            /*Calculamos las coordenadas para dibujar el circulo dependiendo de la escala
             * icq / ADiv = cantidad de divisiones que ocuparemos
             * icq / ADiv * lineas_div = Cantidad de pixeles que vamos a dibujar teniendo en cuenta que 1 division son 20 pixeles
             * (icq / ADiv * lineas_div) - 5 = una pequeña correccion para que quede centrado el circulo
             */
            int icqN = Convert.ToInt32((icq / ADiv * lineas_div) - 5);
            int vceqN = Convert.ToInt32((vceq / VDiv * lineas_div) - 5);

            // Dibujamos el circulo
            grafico.FillEllipse(myBrush, new Rectangle(vceqN, icqN, 10, 10));

            // Llenamos los campos de las escalas, de vcc y de icmax
            lbl_escalaA.Text = Calculos.Notacion(Math.Truncate(ADiv * 10000000) / 10000000, "A") + " / Div";
            lbl_escalaV.Text = Calculos.Notacion(Math.Truncate(VDiv * 10000000) / 10000000, "V") + " / Div";
            lbl_icmax.Text = Calculos.Notacion(Math.Truncate(icmax * 10000000) / 10000000, "A");
            lbl_vcc.Text = Calculos.Notacion(Math.Truncate(vcc * 10000000) / 10000000, "V");
        }

        private void PictureBox1_Paint(object sender, PaintEventArgs e)
        {
            // Dibujamos el grafico apenas se inicia el programa

            int x0 = 20;
            int y0 = pictureBox1.Height - 20;
            int lineas_div = 20;

            e.Graphics.TranslateTransform(x0, y0);
            e.Graphics.ScaleTransform(1, -1);

            Pen lapiz = new Pen(Color.Black, 2);

            //Dibujar ejes
            e.Graphics.DrawLine(lapiz, -10, 0, pictureBox1.Width, 0);
            e.Graphics.DrawLine(lapiz, 0, -10, 0, pictureBox1.Height);

            //Dibujar lineas divisorias
            for (int i = lineas_div; i < pictureBox1.Width; i += lineas_div)
            {
                e.Graphics.DrawLine(lapiz, i, 5, i, -5);
                e.Graphics.DrawLine(lapiz, -5, i, 5, i);
            }
        }
    }
}
