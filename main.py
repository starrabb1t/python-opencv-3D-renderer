import cv2
import renderer as r
import object as o

if __name__ == '__main__':

    while (True):
        camera = r.getCamera(o.verts)

        cv2.imshow('render', r.render(camera, o.edges))
        r.RotY += 0.01
        r.RotX -= 0.005

        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()