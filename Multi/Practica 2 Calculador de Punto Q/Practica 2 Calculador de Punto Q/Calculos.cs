using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Practica_2_Calculador_de_Punto_Q
{
    class Calculos
    {
        public static double[] PuntoQ(double Vfuente, double HFE, double RB, double RC, double RE)
        {
            // Calculamos IB, IC, VCE e ICmax para retornar los valores en un Array
            double IB = (Vfuente - 0.7) / (RB + (HFE * RE));
            
            double IC = IB * HFE;

            double VCE = Vfuente - (RC * IC) - (RE * IC);

            double ICmax = Vfuente / (RC + RE);

            return new[] { IC, VCE, ICmax, Vfuente };
        }

        public static double Verificar(string valor, string unidad)
        {
            // Nos llegan los valores de resistencias con las K o las M y devolvemos el valor ya multiplicado (K = 1000) (M = 1000000)
            switch (unidad)
            {
                case "Ω":
                    return double.Parse(valor);
                case "KΩ":
                    return double.Parse(valor) * 1000;
                case "MΩ":
                    return double.Parse(valor) * 1000000;
                default:
                    return 0;
            }
        }

        public static string Notacion(double num, string unidad)
        {
            // Convertimos los valores que llegan a valores expresados en notacion cientifica (tanto para los Volts como para los Ampers)
            string numS = "";
            if (unidad == "A")
            {
                if (num >= 1)
                {
                    numS = ((num * 1).ToString()) + "A";
                }
                else if (num < 1 && num >= 0.001)
                {
                    numS = ((num * 1000).ToString()) + "mA";
                }
                else if (num < 0.001 && num >= 0.000001)
                {
                    numS = ((num * 1000000).ToString()) + "uA";
                }
                else if (num <= 0)
                {
                    numS = num.ToString() + "A";
                }
            }
            else if (unidad == "V")
            {
                if (num >= 1)
                {
                    numS = ((num * 1).ToString()) + "V";
                }
                else if (num < 1 && num >= 0.001)
                {
                    numS = ((num * 1000).ToString()) + "mV";
                }
                else if (num < 0.001 && num >= 0.000001)
                {
                    numS = ((num * 1000000).ToString()) + "uV";
                }
                else if (num <= 0)
                {
                    numS = num.ToString() + "V";
                }
            }
            else if (unidad == "")
            {
                if (num >= 1)
                {
                    numS = ((num * 1).ToString());
                }
                else if (num < 1 && num >= 0.001)
                {
                    numS = ((num * 1000).ToString());
                }
                else if (num < 0.001 && num >= 0.000001)
                {
                    numS = ((num * 1000000).ToString());
                }
                else if (num <= 0)
                {
                    numS = num.ToString();
                }
            }
            return numS;
        }
    }
}
