# 
# GitHub: @GianK128
#

# Esta debería ser una clase abstracta, pero python no tiene esa funcionalidad (sin modulos)
class Skill():
    def __init__(self, name, description, cooldown, mana_cost, exp_needed, is_unlocked):
        """
            Clase base conteniendo los atributos y metodos necesarios para mantener una habilidad.
        """
        self.__name = name
        self.__description = description
        self.__max_cd = cooldown
        self.__cost = mana_cost
        self.__exp_needed = exp_needed
        self.__is_unlocked = is_unlocked

        self.cd = 0
        # self.reset_cooldown()

    #=====INICIO PROPIEDADES=====#

    @property
    def Name(self):
        return self.__name
    
    @property
    def Description(self):
        return self.__description
    
    @Description.setter
    def Description(self, new_desc):
        self.__description = new_desc

    @property
    def Cooldown(self):
        return self.__max_cd
    
    @Cooldown.setter
    def Cooldown(self, new_cd):
        self.__max_cd = new_cd
    
    @property
    def Cost(self):
        return self.__cost
    
    @Cost.setter
    def Cost(self, new_cost):
        self.__cost = new_cost

    @property
    def EXP(self):
        return self.__exp_needed

    @property
    def Unlocked(self):
        return self.__is_unlocked

    @property
    def ST_details(self):
        return f"{self.__name}:\n{self.__description}\n\nCost: {self.__cost}."
    
    #=====FIN DE PROPIEDADES=====#
    #=====INICIO DE METODOS=====#

    def decrease_cooldown(self, amount):
        self.cd -= amount

    def reset_cooldown(self):
        self.cd = self.__max_cd

    def can_be_unlocked(self, curr_exp):
        return curr_exp >= self.__exp_needed

    def execute_skill(self):
        """
            Ejecuta el codigo para llevar a cabo la habilidad.
        """
        if self.cd <= 0:
            self.reset_cooldown()
            return True
        return False

    #=====FIN DE METODOS=====#

    @classmethod
    def create_empty(cls):
        """
            Crea una instancia de la clase con valores base.
        """
        return cls("", "", 0, 0, 0, False)

class DamageSkill(Skill):
    def __init__(self, name, description, cooldown, mana_cost, exp_needed, is_unlocked, damage_amount = 0, damage_type = ""):
        """
            Instancia de Skill que sirve para habilidades de ataque.
        """
        super().__init__(name, description, cooldown, mana_cost, exp_needed, is_unlocked)
        self.__dmg_amount = damage_amount
        self.__dmg_type = damage_type
    
    def execute_skill(self, atk_position, atk_radius):
        if self.cd <= 0:
            self.reset_cooldown()
            print(f"Attacked at {atk_position} in a space of {atk_radius}!\nI've dealt {self.__dmg_amount} {self.__dmg_type} damage.")
            return True
        return False

class ProtectiveSkill(Skill):
    def __init__(self, name, description, cooldown, mana_cost, exp_needed, is_unlocked, shield_amount = 0, shield_type = ""):
        """
            Instancia de Skill que sirve para habilidades de proteccion.
        """
        super().__init__(name, description, cooldown, mana_cost, exp_needed, is_unlocked)
        self.__shd_amount = shield_amount
        self.__shd_type = shield_type
    
    def execute_skill(self, instance_HP_object):
        if self.cd <= 0:
            self.reset_cooldown()
            print(f"Shielded {instance_HP_object} for {self.__shd_amount} {self.__shd_type} damage.")
            return True
        return False

if __name__ == "__main__":
    sk = Skill("Testname", "", 60, 100, 100, False)
    dmg_sk = DamageSkill("Testname", "", 60, 100, 100, False, 25, "Physical")
    shd_sk = ProtectiveSkill("Testname", "", 60, 100, 100, False, 25, "Magical")

    sk.execute_skill()
    dmg_sk.execute_skill("test", "test")
    shd_sk.execute_skill("test")