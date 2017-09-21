

# Add a patient reference to a doctor (general practitioner)
def add_general_practitioner(patient, doctor):
    patient.general_practitioner = doctor
    patient.save()
