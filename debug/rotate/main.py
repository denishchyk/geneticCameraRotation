import Private_setting

def one_step(camera):

    from debug.trassir import get_img
    f,img = get_img(camera.guid)
    if f and img:
        from debug.img import save_image
        save_image(img, "./images/", camera.name )
        from debug.rotate import genetics
        from debug.img import img_to_frame

        yang = genetics.STEP1_initialize_population_from_frame(img_to_frame(img))

        # TODO модуль детекции переписать
        matches = genetics.STEP2_wedding(camera.old, yang)
        from debug.rotate import angle_of_rotation
        camera.angle = abs(
            angle_of_rotation.calculate_rotation_angle(camera.old, yang, matches)) if camera.keypoint_count > 0 else 0
        camera.turn = camera.angle < Private_setting.threshold
        print(f"угол поворота {camera.angle}")
        if camera.turn:

            next_generation = genetics.STEP3_crossover(yang, camera.old, matches) + genetics.STEP4_selection(yang, matches)

            camera.old = [chromosome for chromosome in next_generation if chromosome.fitness > 1]

        else:

            next_generation = genetics.STEP3_crossover(yang, camera.old, matches) + genetics.STEP4_selection(yang,matches)
            camera.old = [chromosome for chromosome in next_generation if chromosome.fitness > 1]
            (print("((((("))
        for i in camera.old:
            i.fitness -= 1
            #i.save_to_database(name)
        camera.keypoint_count = len(camera.old)

    return camera
